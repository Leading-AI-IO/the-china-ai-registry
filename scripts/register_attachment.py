#!/usr/bin/env python3
"""extract_attachment.py が書き出した附件1本分の行を、data/registry.json の各表の末尾に追加する。

使い方:
    python scripts/register_attachment.py data/staging/attachment_15.json

前提: data/registry.json の sources に、同じ附件番号の項目があり、status が "not_connected" であること
（附件の表題・取得日・公告の情報は、著者が先にそこへ書く。docs/UPDATE_RUNBOOK.md 第1節）。

このスクリプトは次のいずれかに当たると、何も書かずに止まる（docs/DATA_SPEC.md 第6節）:
  - 定義にない表がある（新しい種類の表は、registry.json の tables と docs/DATA_SPEC.md に定義を足してから扱う）
  - PDFのハッシュが sources に書いたものと違う
  - 序号が、その表の最後の序号の次から始まらない、または附件の中で欠番・重複がある
  - 公告本文の件数（sources に書いたもの）と附件の行数が合わず、その食い違いが sources の observations に書かれていない
既存の行は変更しない（追記専用）。
"""
import json
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data" / "registry.json"

ORG_SUFFIX = re.compile(r"(公司|研究院|研究所|大学|学院|集团|中心|医院|委员会|实验室)$")
WHITESPACE = re.compile(r"[\s 　]")
BASE_KEYS = ["id", "seq", "jurisdiction", "name", "entity", "number", "date_raw", "date", "date_note"]


def prefix_of(number):
    return number.split("-", 1)[0].strip().lower()


def observe(rows, by_juris):
    """行ごとの観察コード（docs/DATA_SPEC.md 第5節）。行の値は変えない。"""
    prev = None
    for r in rows:
        obs = []
        if prev is not None and r["seq"] != prev + 1:
            obs.append("SEQ_OUT_OF_ORDER")
        prev = r["seq"]
        if ORG_SUFFIX.search(r["name"]) and not ORG_SUFFIX.search(r["entity"]):
            obs.append("COLUMN_SWAP_SUSPECTED")
        if r["entity"].startswith("司") and not r["entity"].startswith("司法"):
            obs.append("LEADING_CHAR_SUSPECTED")
        if WHITESPACE.search(r["number"]):
            obs.append("WHITESPACE_IN_NUMBER")
        if r.pop("_latin_wrap_fields", []):
            obs.append("LATIN_WRAP_UNRESOLVED")
        counts = by_juris[r["jurisdiction"]]
        top, top_n = counts.most_common(1)[0]
        if prefix_of(r["number"]) != top and counts[prefix_of(r["number"])] == 1 and top_n >= 2:
            obs.append("PREFIX_VARIANT")
        r["observations"] = obs


def main():
    staged = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    reg = json.loads(REG.read_text(encoding="utf-8"))
    defs = reg["tables"]
    n = staged["attachment"]

    unknown = [k for k in staged["tables"] if k not in defs]
    if unknown:
        sys.exit(f"定義にない表 {unknown}。registry.json の tables と docs/DATA_SPEC.md に定義を足してから扱う")
    src = next((s for s in reg["sources"] if s.get("attachment") == n), None)
    if src is None:
        sys.exit(f"sources に附件{n}の項目がない。先に表題・取得日・公告の情報を書くこと。")
    if src["status"] != "not_connected":
        sys.exit(f"附件{n}の status が {src['status']}。連結済みの附件は追加しない（追記専用）。")
    if src.get("file_sha256") and src["file_sha256"] != staged["file_sha256"]:
        sys.exit(f"PDFのハッシュが sources と違う: {staged['file_sha256']}")

    # 序号の連続性
    for key, rows in staged["tables"].items():
        last = max((r["seq"] for r in reg[key]), default=0)
        seqs = sorted(r["seq"] for r in rows)
        if seqs[0] != last + 1:
            sys.exit(f"{key}: 附件{n}の最初の序号 {seqs[0]} が、台帳の最後の序号 {last} の次ではない")
        if seqs != list(range(seqs[0], seqs[0] + len(seqs))):
            sys.exit(f"{key}: 附件{n}の中に欠番または重複がある")

    # 公告本文の件数との照合
    stated = (src.get("notice") or {}).get("stated") or {}
    mismatch = []
    for group in ("filings", "registrations"):
        keys = [k for k, d in defs.items() if d["counts_toward"] == group]
        new_rows = sum(len(staged["tables"].get(k, [])) for k in keys)
        cum = sum(max([r["seq"] for r in reg[k] + staged["tables"].get(k, [])], default=0) for k in keys)
        if stated.get(f"new_{group}") is not None and stated[f"new_{group}"] != new_rows:
            mismatch.append((group, f"new {stated[f'new_{group}']} != rows {new_rows}"))
        if stated.get(f"cumulative_{group}") is not None and stated[f"cumulative_{group}"] != cum:
            mismatch.append((group, f"cumulative {stated[f'cumulative_{group}']} != sum of last seqs {cum}"))
    for key, d in defs.items():
        sk = d.get("stated_key")
        if sk and stated.get(sk) is not None and stated[sk] != len(staged["tables"].get(key, [])):
            mismatch.append((key, f"{sk} {stated[sk]} != rows {len(staged['tables'].get(key, []))}"))
    documented = {o.get("table") for o in src.get("observations", []) if o.get("code") == "COUNT_MISMATCH_WITH_NOTICE"}
    undocumented = [m for m in mismatch if m[0] not in documented]
    if undocumented:
        sys.exit(f"公告本文と附件の件数が合わない: {undocumented}。食い違いを sources の observations に記録してから実行すること。")

    all_existing = [r for k in defs for r in reg[k]]
    all_staged = [r for rows in staged["tables"].values() for r in rows]
    by_juris = {}
    for r in all_existing + all_staged:
        by_juris.setdefault(r["jurisdiction"], Counter())[prefix_of(r["number"])] += 1

    summary = {}
    for key in defs:
        rows = staged["tables"].get(key, [])
        d = defs[key]
        observe(rows, by_juris)
        for r in rows:
            r["id"] = f"{d['id_prefix']}{r['seq']:04d}"
            r["source"] = {"attachment": n, **r["source"]}
            if key == "filing_changes":
                filing_rows = [x for k, dd in defs.items() if dd["counts_toward"] == "filings" for x in reg[k]]
                hits = [x["id"] for x in filing_rows if x["number"] == r["number"]]
                r["target_id"] = hits[0] if len(hits) == 1 else None
                if len(hits) == 0:
                    r["observations"].append("TARGET_NOT_FOUND")
                elif len(hits) > 1:
                    r["observations"].append("TARGET_AMBIGUOUS")
        keys = BASE_KEYS + d.get("extra_fields", []) + ["source", "observations"]
        reg[key].extend({k: r.get(k) for k in keys} for r in rows)
        seqs = [r["seq"] for r in rows]
        summary[key] = {"count": len(rows), "seq_min": min(seqs) if seqs else None, "seq_max": max(seqs) if seqs else None}

    src.update({
        "file_name": src.get("file_name") or staged["file_name"],
        "file_sha256": staged["file_sha256"],
        "pages": staged["pages"],
        "extractor": staged["extractor"],
        "headers": staged["headers"],
        "tables": summary,
        "status": "connected",
    })
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"附件{n}を連結: " + "、".join(f"{k} {v['count']}行" for k, v in summary.items() if v["count"]))


if __name__ == "__main__":
    main()
