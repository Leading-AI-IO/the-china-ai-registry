#!/usr/bin/env python3
"""CACの附件（PDF）1本から、表ごとに行を転記して JSON に書き出す。

使い方:
    python scripts/extract_attachment.py --attachment 15 --pdf <附件のPDF> --out data/staging/attachment_15.json

この段階では data/registry.json に触れない。台帳への追加は scripts/register_attachment.py で行う。

転記の規律（docs/DATA_SPEC.md 第3節）:
  - 原表の列位置のまま写す。列のずれ・誤字・混入を直さない
  - セル内の改行（PDFの折り返し）と、セル両端の空白だけを取り除く。セル内部の空白は残す
  - 文字を足さない。翻訳しない。簡体字のまま
同じPDFと同じ pdfplumber の版からは、同じ出力が得られる（決定的）。

表の判定（docs/DATA_SPEC.md 第2節）:
  1. 表の直前にある表題の文字列（TITLES）で決める。表題がページの末尾にあり、表が次のページから始まる場合も拾う
  2. 表題が取り出せない附件（附件1〜5・8）では、見出し行の文言（「应用/功能名称」なら登記）で決める
  3. 見出し行の直後の序号が、備案の表でそれまでに出た最大の序号より小さければ、登記の表の始まりとみなす
     （附件8は登記の表題が取り出せず、見出しも備案と同じ文言のため）
  4. どれにも当たらなければ、直前の表の続きとみなす
未知の表題・見出しに当たった場合は、何も書かずに止まる（新しい種類の表は、定義を足してから扱う）。
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

import pdfplumber

PDFPLUMBER_VERSION = "0.11.10"
TABLE_SETTINGS = {"text_keep_blank_chars": True}

# 表題 → 表のキー。長い（具体的な）表題から順に照合する
TITLES = [
    ("拟人化互动服务场景生成式人工智能服务已备案信息", "filings_anthropomorphic"),
    ("提供手机端侧生成式人工智能服务已备案信息", "filings_on_device"),
    ("生成式人工智能服务已备案变更信息", "filing_changes"),
    ("生成式人工智能服务已登记信息", "registrations"),
    ("生成式人工智能服务已备案信息", "filings"),
]
# 原表の見出し → 欄のキー
HEADER_MAP = {
    "序号": "seq",
    "属地": "jurisdiction",
    "模型名称": "name", "大模型名称": "name", "应用/功能名称": "name", "大模型": "name",
    "备案单位": "entity", "登记单位": "entity",
    "备案号": "number", "备案编号": "number", "上线编号": "number",
    "备案时间": "date_raw", "登记时间": "date_raw",
    "适用场景": "scenario",
    "变更时间": "changed_raw",
}
DATE_RE = re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})(.*)$")
LATIN_WRAP_RE = re.compile(r"[A-Za-z0-9]\n[A-Za-z0-9]")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize(cell):
    """改行を取り除き、両端の空白を取り除く。それ以外は変えない。"""
    if cell is None:
        return ""
    return cell.replace("\n", "").strip()


def parse_date(raw):
    m = DATE_RE.match(raw)
    if not m:
        return None, None
    y, mo, d, rest = m.groups()
    return datetime.date(int(y), int(mo), int(d)).isoformat(), (rest.strip() or None)


def title_in(text):
    compact = re.sub(r"\s", "", text or "")
    for title, key in TITLES:
        if title in compact:
            return key
    return None


def region_text(page, top, bottom):
    if bottom - top < 1:
        return ""
    return page.crop((0, top, page.width, bottom)).extract_text() or ""


def extract(pdf_path):
    tables = {}          # key -> rows
    headers = {}         # key -> 原表の見出し
    order = {}
    current = "filings"
    pending = None       # 前のページの末尾で見つけた表題
    field_map = None
    header_pending = False   # 見出し行の直後かどうか（規則3）
    max_filing_seq = 0

    if pdfplumber.__version__ != PDFPLUMBER_VERSION:
        print(f"警告: pdfplumber {pdfplumber.__version__}（規定は {PDFPLUMBER_VERSION}）。出力が変わりうる。", file=sys.stderr)

    with pdfplumber.open(pdf_path) as pdf:
        pages = len(pdf.pages)
        for page_no, page in enumerate(pdf.pages, start=1):
            found = sorted(page.find_tables(TABLE_SETTINGS), key=lambda t: t.bbox[1])
            prev_bottom = 0
            for t in found:
                key = title_in(region_text(page, prev_bottom, t.bbox[1])) or pending
                pending = None
                if key:
                    current = key
                    field_map = None
                prev_bottom = t.bbox[3]
                for cells in t.extract(keep_blank_chars=True):
                    first = normalize(cells[0])
                    if first == "序号":
                        names = [normalize(c) for c in cells]
                        unknown = [n for n in names if n not in HEADER_MAP]
                        if unknown:
                            raise SystemExit(f"未知の見出し {unknown}: p.{page_no}。docs/DATA_SPEC.md に定義を足してから扱う")
                        if not key and "应用/功能名称" in names:
                            current = "registrations"
                        field_map = [HEADER_MAP[n] for n in names]
                        header_names = names
                        header_pending = not key
                        if current != "filings" or key:
                            headers.setdefault(current, names)
                        continue
                    if field_map is None:
                        raise SystemExit(f"見出しのない表: p.{page_no} {cells}")
                    if len(cells) != len(field_map):
                        raise SystemExit(f"列数が見出しと合わない行: p.{page_no} {cells}")
                    if not first.isdigit():
                        raise SystemExit(f"序号が数字でない行: p.{page_no} {cells}")
                    if header_pending:
                        header_pending = False
                        if current == "filings" and max_filing_seq and int(first) < max_filing_seq:
                            current = "registrations"
                        headers.setdefault(current, header_names)
                    if current == "filings":
                        max_filing_seq = max(max_filing_seq, int(first))
                    raw = dict(zip(field_map, cells))
                    row = {k: normalize(v) for k, v in raw.items()}
                    row["seq"] = int(row["seq"])
                    row["date"], row["date_note"] = parse_date(row["date_raw"])
                    if row["date"] is None:
                        raise SystemExit(f"日付を読めない行: p.{page_no} {cells}")
                    if "changed_raw" in row:
                        row["changed"], row["changed_note"] = parse_date(row["changed_raw"])
                        if row["changed"] is None:
                            raise SystemExit(f"変更時間を読めない行: p.{page_no} {cells}")
                    order[current] = order.get(current, 0) + 1
                    row["source"] = {"page": page_no, "order": order[current]}
                    row["_latin_wrap_fields"] = [k for k in ("jurisdiction", "name", "entity")
                                                 if raw.get(k) and LATIN_WRAP_RE.search(raw[k])]
                    tables.setdefault(current, []).append(row)
            pending = title_in(region_text(page, prev_bottom, page.height))
    return tables, headers, pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attachment", type=int, required=True, help="附件番号（CACのハブページの番号）")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    pdf_path = pathlib.Path(args.pdf)
    tables, headers, pages = extract(pdf_path)
    out = {
        "attachment": args.attachment,
        "file_name": pdf_path.name,
        "file_sha256": sha256(pdf_path),
        "pages": pages,
        "extractor": {"tool": "pdfplumber", "version": pdfplumber.__version__, "table_settings": TABLE_SETTINGS},
        "headers": headers,
        "tables": tables,
    }
    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for k, rows in tables.items():
        print(f"{k}: {len(rows)}行（序号 {min(r['seq'] for r in rows)}〜{max(r['seq'] for r in rows)}）")


if __name__ == "__main__":
    main()
