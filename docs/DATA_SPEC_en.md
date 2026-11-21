# The China AI Registry — Data Specification

This file defines what the registry data in `data/` records and under which rules. Operating procedures are in `docs/UPDATE_RUNBOOK_en.md`. The Japanese version (`docs/DATA_SPEC.md`) is authoritative.

**Established**: 2026-11-22 (v1.3, Attachments 1–14)

---

## 1. Population

The registry records **every row listed in the attachments** to the notices "Generative AI services filed (and registered)" (生成式人工智能服务已备案（和已登记）信息) published by the Cyberspace Administration of China (CAC).

- The population is defined by CAC. The author does not select rows; every row of a connected attachment is admitted without exception
- Only rows printed in an attachment PDF are admitted. No row is created from press reports, provincial cyberspace offices, or company announcements
- Each attachment is a delta, not a cumulative list (Chapter 1). The full population exists only when attachments are joined in order from Attachment 1
- No row is created from a notice that carries no serial numbers (e.g., the notice of 23 September 2026 on three on-device services, whose details are an image). Such notices are recorded in `separate_notices` in `registry.json`, and the services are admitted as rows of a later attachment if they appear there with serial numbers

## 2. Tables (one per serial-number series)

**Principle: one serial-number series is one table.** If CAC adds a table with a new series, a definition is added here and to `tables` in `registry.json` before connecting (the scripts stop on an undefined table).

| Table | Key | ID prefix | Source title | First attachment | Counted in the notice's cumulative |
|---|---|---|---|---|---|
| Filings | `filings` | F | 生成式人工智能服务已备案信息 | 1 | filings |
| On-device filings | `filings_on_device` | D | 提供手机端侧生成式人工智能服务已备案信息 | 13 | filings |
| Anthropomorphic-interaction filings | `filings_anthropomorphic` | A | 拟人化互动服务场景生成式人工智能服务已备案信息 | 14 | filings |
| Registrations | `registrations` | R | 生成式人工智能服务已登记信息 | 2 | registrations |
| Filing changes | `filing_changes` | C | 生成式人工智能服务已备案变更信息 | 14 | none |

- The three filing tables are separate series each starting at 1, but the notice's cumulative filings are their sum (as of Attachment 14: 1,234 + 10 + 1 = 1,245). Filings and registrations are **never added together**
- A filing change records that information of an already filed service (such as the entity name) changed. **The original filing row is not rewritten; the change is appended to this table**, and `target_id` points to the original row
- Registrations begin with Attachment 2 (August 2024)

## 3. Transcription rules

1. **Copy cells in their source column positions.** Rows whose columns are shifted (e.g., Nos. 340–345) are not corrected. Correction is interpretation, not transcription
2. **Add, delete or replace no characters.** Only space glyphs present in the PDF count as spaces (gaps between characters do not). Two removals only:
   - line breaks inside a cell (created by wrapping in the PDF)
   - whitespace at both ends of a cell
   Whitespace inside a cell (ASCII, full-width, repeated, no-break space) is kept. Where a space glyph sits at a wrap point, that space is kept
3. **Typos, carry-overs and spelling variants are not corrected.** Anything noticed is recorded in `observations` (Section 5)
4. **No translation.** Values are kept in Simplified Chinese. Japanese and English names are given in the body text
5. **No interpretive fields.** Industry, entity resolution, foreign-owned status and assessments of success are not part of the data layer. They belong to the body text (the analysis layer), which states the data version it used

Transcription is done by `scripts/extract_attachment.py`. The same PDF and the same pdfplumber version (0.11.10) always produce the same output.

## 4. Fields

### 4-1. Rows (shared by `filings` and `registrations`)

| Key | Meaning | Source header (filings / registrations) | Rule |
|---|---|---|---|
| `id` | Row ID | none | `F` + 4-digit serial for filings; `R` + 4-digit serial for registrations |
| `seq` | Serial number | 序号 | As printed |
| `jurisdiction` | Jurisdiction | 属地 | As printed; 国资委 is treated as a jurisdiction |
| `name` | Name | 模型名称・大模型名称 / 应用/功能名称 | As printed |
| `entity` | Entity | 备案单位 / 登记单位 | As printed |
| `number` | Number | 备案号・备案编号 / 上线编号 | As printed |
| `date_raw` | Date as printed | 备案时间 / 登记时间 | As printed, including annotations such as （补登） |
| `date` | Date | none | Date part of `date_raw` as YYYY-MM-DD |
| `date_note` | Date annotation | none | Text after the date in `date_raw` (e.g., （补登）), or `null` |
| `source.attachment` | Attachment number | none | Number on CAC's hub page |
| `source.page` | Page | none | PDF page (from 1) |
| `source.order` | Order | none | Position in the source table of that attachment (from 1) |
| `observations` | Observations | none | Array of codes from Section 5. Values are not altered |
| `scenario` | Applicable scenario | 适用场景 | Only in on-device and anthropomorphic filings and in filing changes. As printed (including '/') |
| `changed_raw`, `changed`, `changed_note` | Change date | 变更时间 | Only in filing changes; same rules as `date_raw`, `date`, `date_note` |
| `target_id` | Target row | none | Only in filing changes: ID of the filing row (F, D or A) whose number matches exactly, or `null` |
| `corrections` | Corrections | none | Present only when a transcription error is found: date, field, value as printed (`as_printed`), reason. The original value is not rewritten (`UPDATE_RUNBOOK_en.md` Section 4) |

From Attachment 6 on, the registration tables carry the same header text as the filing tables (大模型名称・备案单位・备案编号・备案时间). Keys are unified by column position; the original headers of each attachment are kept in `sources[].headers`.

### 4-2. Sources (`sources`)

One entry per attachment, created as soon as the attachment is known to exist, connected or not.

| Key | Meaning |
|---|---|
| `attachment` | Attachment number |
| `status` | `connected` / `not_connected` |
| `hub_url`, `hub_label` | Hub page URL and the attachment label shown there |
| `pdf_title` | Title printed in the PDF, as far as it can be extracted as text; otherwise `null` with `pdf_title_note` |
| `file_name`, `file_sha256`, `pages` | File name, SHA-256 and page count of the PDF used. Readers can confirm they hold the same file |
| `retrieved` | Date the PDF was retrieved |
| `extractor` | Tool, version and settings used |
| `headers` | Original table headers (filings, registrations) |
| `notice` | Notice URL, date, title and the counts stated in the notice body (`stated`). Only values confirmed on the CAC notice page are recorded; press figures are not |
| `notice.stated` | Counts in the notice body: new filings (`new_filings`, the sum of the three filing tables), new registrations, cumulative totals, as-of date, and, where the notice breaks them down, `new_filings_on_device`, `new_filings_anthropomorphic`, `changed_filings` |
| `tables` | Connected row count and serial-number range per table |
| `observations` | Attachment-level observations (Section 5) |

The PDFs themselves are not included in the repository; the originals are on CAC's hub page.

## 5. Observation codes

An observation records something noticed about the source. **Values are never altered because of an observation.** Row observations are assigned by rule at connection time by `register_attachment.py` and not changed afterwards.

| Code | Condition |
|---|---|
| `SEQ_OUT_OF_ORDER` | In source order, the serial number is not the previous row's plus one |
| `COLUMN_SWAP_SUSPECTED` | The name ends with an organisation suffix (公司・研究院・研究所・大学・学院・集团・中心・医院・委员会・实验室) and the entity does not |
| `LEADING_CHAR_SUSPECTED` | The entity begins with 司 (other than 司法) |
| `WHITESPACE_IN_NUMBER` | Whitespace inside the number |
| `LATIN_WRAP_UNRESOLVED` | The source cell wraps between two Latin alphanumerics with no space glyph at the wrap; joined without a space |
| `PREFIX_VARIANT` | The number prefix (before the first hyphen) matches no other row of the same jurisdiction at connection time (case-insensitive) |
| `TARGET_NOT_FOUND` | No filing row has exactly the number given in a change row |
| `TARGET_AMBIGUOUS` | More than one filing row matches the number in a change row |

Attachment-level observations:

| Code | Condition |
|---|---|
| `COUNT_MISMATCH_WITH_NOTICE` | The attachment's row count or last serial number differs from the notice body. Both are recorded unchanged |
| `SOURCE_FILE_CHANGED` | CAC replaced the PDF of the same attachment and its hash changed. Existing rows are not rewritten; differences go into each row's `corrections` |

The rules are mechanical and are not guaranteed to catch every anomaly. Errors they miss are handled under Section 4 of the runbook.

## 6. Checks

The scripts stop without writing anything if any of the following holds.

**At connection (`register_attachment.py`)**
- The PDF hash differs from the one already written in `sources`
- An undefined table is present
- The attachment's first serial number does not follow the last one of that table
- Gaps or duplicates within the attachment
- The notice counts (new, cumulative, breakdown) and the attachment row counts differ and the difference is not recorded in `sources[].observations`
- The attachment has already been connected

**At build (`build_registry.py`)**
- Serial numbers do not run from 1 without gaps or duplicates
- `id` does not match the serial number, or is duplicated
- A required field (jurisdiction, name, entity, number, date as printed) is empty
- `date` (and `changed` in filing changes) is not YYYY-MM-DD
- `target_id` points to a row not in the registry
- An undefined observation code is used
- A `corrections` entry lacks date, field or `as_printed`
- Row counts or serial ranges of connected attachments disagree with `sources`

## 7. Files

| File | Type | Content |
|---|---|---|
| `data/registry.json` | Canonical | Definitions, sources, all rows. Edited only through the scripts |
| `data/filings.csv` | Derived | Filings. UTF-8 with BOM, as are all CSVs below |
| `data/filings_on_device.csv` | Derived | On-device filings |
| `data/filings_anthropomorphic.csv` | Derived | Anthropomorphic-interaction filings |
| `data/registrations.csv` | Derived | Registrations |
| `data/filing_changes.csv` | Derived | Filing changes |
| `data/sources.csv` | Derived | Source and connection status per attachment |
| `scripts/extract_attachment.py` | Tool | PDF → staging file (`data/staging/`, not committed) |
| `scripts/register_attachment.py` | Tool | Staging file → end of `registry.json` |
| `scripts/build_registry.py` | Tool | Checks and generation of derived files |

In the CSVs, `observations` lists codes and `corrections` lists `date:field`, each separated by `;`.

## 8. What this data cannot tell you

- A filing means only that a service was filed. Whether the deployments on the list succeed cannot be read from this data
- The number of filings is not the number of companies. The same legal entity holds several rows, and the same brand is filed under different legal entities. CAC's tables have no column for resolving entities
- The scope is services the authorities judged to have "public-opinion attributes or social mobilisation capability", not every AI model in China
