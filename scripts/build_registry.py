#!/usr/bin/env python3
"""data/registry.json（正本）を検査し、CSVを生成する。

使い方:
    python scripts/build_registry.py

生成物（すべて registry.json から生成し、同じコミットに入れる）:
    data/<表のキー>.csv   registry.json の tables に定義した表ごとに1つ
                          （filings・filings_on_device・filings_anthropomorphic・registrations・filing_changes）
    data/sources.csv      附件ごとの出典と連結の状態

検査（docs/DATA_SPEC.md 第6節）に1つでも当たれば、何も書かずに止まる。
"""
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REG = DATA / "registry.json"

BASE_COLS = ["id", "seq", "jurisdiction", "name", "entity", "number", "date_raw", "date", "date_note"]
TAIL_COLS = ["attachment", "page", "order", "observations", "corrections"]
REQUIRED = ["jurisdiction", "name", "entity", "number", "date_raw"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(errors):
    for e in errors:
        print("NG:", e, file=sys.stderr)
    sys.exit(1)


def validate(reg):
    errors = []
    defs = reg["tables"]
    codes = set(reg["observation_codes"])
    src_codes = set(reg["source_observation_codes"])
    connected = {s["attachment"]: s for s in reg["sources"] if s["status"] == "connected"}
    all_ids = {r["id"] for k in defs for r in reg[k]}
    for key, d in defs.items():
        rows = reg.get(key)
        if rows is None:
            errors.append(f"表 {key} が registry.json にない")
            continue
        seqs = [r["seq"] for r in rows]
        if sorted(seqs) != list(range(1, len(seqs) + 1)):
            errors.append(f"{key}: 序号が1から欠番・重複なく続いていない")
        id_re = re.compile(rf"^{d['id_prefix']}\d{{4,}}$")
        for r in rows:
            if not id_re.match(r["id"]) or int(r["id"][len(d["id_prefix"]):]) != r["seq"]:
                errors.append(f"{key} {r['id']}: id と序号が対応しない")
            for k in REQUIRED + d.get("required_extra", []):
                if not r.get(k):
                    errors.append(f"{key} {r['id']}: {k} が空")
            for k in ("date",) + (("changed",) if "changed" in d.get("extra_fields", []) else ()):
                if not DATE_RE.match(r.get(k) or ""):
                    errors.append(f"{key} {r['id']}: {k} が YYYY-MM-DD でない")
            if "target_id" in d.get("extra_fields", []) and r.get("target_id") and r["target_id"] not in all_ids:
                errors.append(f"{key} {r['id']}: target_id {r['target_id']} が台帳にない")
            for o in r["observations"]:
                if o not in codes:
                    errors.append(f"{key} {r['id']}: 未定義の観察コード {o}")
            for c in r.get("corrections", []):
                if not (DATE_RE.match(c.get("date", "")) and c.get("field") in r and "as_printed" in c):
                    errors.append(f"{key} {r['id']}: corrections の項目に date・field・as_printed が揃っていない")
            if r["source"]["attachment"] not in connected:
                errors.append(f"{key} {r['id']}: 連結済みでない附件を出典としている")
        for n, s in connected.items():
            got = [r["seq"] for r in rows if r["source"]["attachment"] == n]
            meta = (s.get("tables") or {}).get(key, {"count": 0, "seq_min": None, "seq_max": None})
            if len(got) != meta["count"]:
                errors.append(f"{key}: 附件{n}の行数 {len(got)} が sources の count {meta['count']} と違う")
            if got and (min(got) != meta["seq_min"] or max(got) != meta["seq_max"]):
                errors.append(f"{key}: 附件{n}の序号の範囲が sources と違う")
    for s in reg["sources"]:
        if s["status"] not in ("connected", "not_connected"):
            errors.append(f"附件{s['attachment']}: status が未定義 {s['status']}")
        for o in s.get("observations", []):
            if o.get("code") not in src_codes:
                errors.append(f"附件{s['attachment']}: 未定義の観察コード {o.get('code')}")
    return errors


def flat_row(r, extra):
    out = {k: r.get(k) if r.get(k) is not None else "" for k in BASE_COLS + extra}
    out.update({
        "attachment": r["source"]["attachment"],
        "page": r["source"]["page"],
        "order": r["source"]["order"],
        "observations": ";".join(r["observations"]),
        "corrections": ";".join(c["date"] + ":" + c["field"] for c in r.get("corrections", [])),
    })
    return out


def source_cols(defs):
    cols = ["attachment", "status", "hub_label", "pdf_title", "file_name", "file_sha256", "pages", "retrieved",
            "notice_url", "notice_date", "stated_new_filings", "stated_new_registrations",
            "stated_cumulative_filings", "stated_cumulative_registrations"]
    for k in defs:
        cols += [f"{k}_count", f"{k}_seq_min", f"{k}_seq_max"]
    return cols + ["observations"]


def flat_source(s, defs):
    notice = s.get("notice") or {}
    stated = notice.get("stated") or {}
    out = {
        "attachment": s["attachment"], "status": s["status"], "hub_label": s.get("hub_label") or "",
        "pdf_title": s.get("pdf_title") or "", "file_name": s.get("file_name") or "",
        "file_sha256": s.get("file_sha256") or "", "pages": s.get("pages") or "", "retrieved": s.get("retrieved") or "",
        "notice_url": notice.get("url", ""), "notice_date": notice.get("date", ""),
        "observations": ";".join(o["code"] for o in s.get("observations", [])),
    }
    for k in ("new_filings", "new_registrations", "cumulative_filings", "cumulative_registrations"):
        out[f"stated_{k}"] = stated.get(k, "")
    for k in defs:
        t = (s.get("tables") or {}).get(k) or {}
        out[f"{k}_count"] = t.get("count", "") if s["status"] == "connected" else ""
        out[f"{k}_seq_min"] = t.get("seq_min") or ""
        out[f"{k}_seq_max"] = t.get("seq_max") or ""
    return out


def write_csv(path, cols, rows):
    # UTF-8（BOM付き）：表計算ソフトで開いたときに簡体字が化けないようにする
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main():
    reg = json.loads(REG.read_text(encoding="utf-8"))
    errors = validate(reg)
    if errors:
        fail(errors)
    defs = reg["tables"]
    for key, d in defs.items():
        extra = d.get("extra_fields", [])
        write_csv(DATA / f"{key}.csv", BASE_COLS + extra + TAIL_COLS, [flat_row(r, extra) for r in reg[key]])
    write_csv(DATA / "sources.csv", source_cols(defs), [flat_source(s, defs) for s in reg["sources"]])
    counts = "、".join(f"{key} {len(reg[key])}行" for key in defs)
    print(f"OK: {counts}／附件 {len(reg['sources'])}件（連結済み {sum(s['status'] == 'connected' for s in reg['sources'])}）")


if __name__ == "__main__":
    main()
