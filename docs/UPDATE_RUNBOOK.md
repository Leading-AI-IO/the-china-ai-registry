# The China AI Registry — 更新手順書

このファイルは公開されている。台帳に書くのは著者一人であり、その一人が実際にどの手順で附件を連結し、誤りを訂正しているかを、読者が検証できる状態に置くためである。データの定義は `docs/DATA_SPEC.md` にある。

**対象リポジトリ**：`https://github.com/Leading-AI-IO/the-china-ai-registry`
**署名鍵**：`3DD95BA9EC194524`（`Satoshi Yamauchi <s3atoshi@gmail.com>`・ed25519）。`the-ai-forecast-registry`・`the-japan-breach-registry-2026` と同じ鍵。秘密鍵はここに含まれない。
**最終更新**：2026-11-22（v1.3・附件1〜14を連結。備案1,234行・端末側の備案10行・擬人化された対話の備案1行・登記955行・備案の変更1行）

---

## この手順書が守っているもの

1. **母集団はCACが決める** ── 連結した附件の行は例外なくすべて収め、附件にない行は起こさない
2. **転記は直さない** ── 原表の列位置・文字のまま写す。気づいたことは観察コードで記録する
3. **追記専用** ── 行を削除も書き換えもしない。訂正は、訂正である旨と日付を明記して追記する
4. **正本と派生物は同時更新** ── `data/registry.json` をスクリプトで更新し、`scripts/build_registry.py` でCSVを生成し、同じコミットに入れる
5. **全コミットに署名、秘密鍵はリポジトリに入れない**

手順の途中で迷ったら、その操作が上の5つのどれを守るためのものかに戻ること。

---

## 周期

**月1回程度を目安に、ハブページ（`https://www.cac.gov.cn/2024-04/02/c_1713729983803145.htm`）を確認する。** 厳格な期限は設けない。

- CACは2ヶ月ごとに、直前の2ヶ月分の附件を公告する（2026年は5月13日・7月10日・9月14日）。月1回の確認で、各附件をおおむね1ヶ月以内に拾える
- 新しい附件があれば連結し、版を上げる。複数の附件がたまっていれば、まとめて連結してよい
- 附件の連結が遅れても、台帳の正しさは損なわれない。附件は差分名簿であり、後から順に連結すれば全数が揃う

---

## 0. 作業前の確認（毎回）

```powershell
cd <リポジトリのクローン先>
git remote -v
git fetch origin
git log --oneline HEAD..origin/main
git status
Get-ChildItem -Recurse -File -Include *.asc,*.rev,*.gpg,*.key,*.pgp
pip show pdfplumber
```

- `git log --oneline HEAD..origin/main` の出力が空であること（空でなければ `git pull --no-rebase --no-edit`）
- `git status` が `nothing to commit, working tree clean` であること
- 鍵ファイルの検索が何も表示しないこと
- pdfplumber の版が `0.11.10` であること（違うと転記の結果が変わりうる。`pip install pdfplumber==0.11.10`）

---

## 1. 新しい附件を連結する

### 1-1. 公告と附件を確認する

1. ハブページで、新しい附件の番号と表題を確認する
2. その期の公告ページを開き、日付・表題・本文の件数（新規の備案・新規の登記・累計の備案・累計の登記・基準日）を確認する
3. 附件のPDFをダウンロードし、リポジトリの**外**に保存する（例：`..\cac-attachments\14_2026-10.pdf`）。PDFはコミットしない

報道の数字は使わない。公告ページに到達できない場合は、`notice` を `null` のままにして連結し、`pending_checks` にその旨を書く。

### 1-2. `sources` に項目を書く

`data/registry.json` の `sources` の該当する附件の項目（なければ末尾に追加）に、次を手で書く。**行（`filings`・`registrations`）は手で編集しない。**

```json
{
  "attachment": 14,
  "status": "not_connected",
  "hub_url": "https://www.cac.gov.cn/2024-04/02/c_1713729983803145.htm",
  "hub_label": "附件14：生成式人工智能服务已备案和已登记信息（2026年10月）",
  "retrieved": "YYYY-MM-DD",
  "notice": {
    "url": "<公告ページのURL>",
    "date": "YYYY-MM-DD",
    "title": "<公告の表題>",
    "stated": {"new_filings": 0, "new_registrations": 0, "cumulative_filings": 0, "cumulative_registrations": 0, "as_of": "YYYY-MM-DD"}
  },
  "observations": []
}
```

### 1-3. 転記して連結する

```powershell
python scripts/extract_attachment.py --attachment 14 --pdf ..\cac-attachments\14_2026-10.pdf --out data/staging/attachment_14.json
python scripts/register_attachment.py data/staging/attachment_14.json
python scripts/build_registry.py
```

- `extract_attachment.py` が表示する表ごとの行数と序号の範囲が、公告本文の件数と合っていること
- **見たことのない表題・見出しの表があると、`extract_attachment.py` は止まる。** CACが新しい種類の表を加えたということである。`docs/DATA_SPEC.md` 第2節の原則（1つの序号の系列を1つの表にする）に従って、`DATA_SPEC.md`・`registry.json` の `tables`・`extract_attachment.py` の `TITLES`／`HEADER_MAP` に定義を足し、日付つきで記録してから連結する
- `register_attachment.py` が止まった場合は、表示された理由を直す。**件数が公告本文と合わないときは、附件の行を足したり削ったりしない。** 食い違いを `sources` の該当項目の `observations` に、次の形で書いてから再実行する

```json
{"code": "COUNT_MISMATCH_WITH_NOTICE", "table": "registrations", "note": {"ja": "公告本文の新規の登記はN件、附件の行数はM行", "en": "The notice states N new registrations; the attachment has M rows"}, "recorded": "YYYY-MM-DD"}
```

- `build_registry.py` が `OK:` を表示すること

### 1-4. 新しい行を目で確かめる

`data/filings.csv`・`data/registrations.csv` の追加分を開き、PDFと次を突き合わせる。

- 先頭の3行と末尾の3行（序号・名称・単位・番号・時間）
- 観察コードが付いた行のすべて
- ページの境目にある行（`page` が変わる直前と直後）

食い違いがあれば、転記の道具の問題である。行を手で直さず、第4節に従う。

### 1-5. 本文・READMEを更新する

- `version` と `snapshot_date` を `registry.json` で更新する
- READMEの更新履歴に版を1行追加する（版・日付・連結した附件・行数）
- 本文で件数・分布に触れる箇所は、**（YYYY年M月D日追記）を前置して追記し、元の記述は残す**
- `llms.txt` の件数を更新する

### 1-6. コミットして push

```powershell
git add data/registry.json data/filings.csv data/filings_on_device.csv data/filings_anthropomorphic.csv data/registrations.csv data/filing_changes.csv data/sources.csv README.md README_en.md llms.txt docs/jp/the-china-ai-registry_JP.md docs/en/the-china-ai-registry_EN.md
git status
git diff --cached --stat
git commit -S -m "Connect attachment 14 (2026-10): filings N–M, registrations N–M"
git show --stat HEAD
git push
git verify-commit HEAD
```

- `git add -A` は使わない（`data/staging/` や鍵ファイルを巻き込まないため）
- `git verify-commit HEAD` が `Good signature from "Satoshi Yamauchi <s3atoshi@gmail.com>"` を返すこと
- 署名つきタグ（`git tag -s v1.4 -m "v1.4"`）を付けて push し、GitHubのReleasesに版を作る

---

## 2. 序号を持たない公告が出た場合

2026年9月23日の端末側3件のように、2ヶ月ごとの附件とは別に公告が出ることがある。

1. `registry.json` の `separate_notices` に、日付・URL・表題・状態（`not_in_registry`）・理由を追記する
2. 行は起こさない
3. 次の附件を連結したときに、その公告のサービスが序号つきで載っているかを確かめ、`separate_notices` の該当項目に結果を（YYYY年M月D日追記）で書く

---

## 3. 公告本文の件数を後から確認した場合

`pending_checks` にある公告本文（附件1〜10など）を確認したら、`sources[].notice` に書き、`build_registry.py` を実行する。附件の行数と合わない場合は、`COUNT_MISMATCH_WITH_NOTICE` を `observations` に追記する。行は変えない。`pending_checks` の該当項目には、（YYYY年M月D日追記）で確認の結果を書く。

コミット件名は `Record notice for attachment N`。

---

## 4. 誤りに気づいた場合

行の値は書き換えない。誤りの種類で扱いを分ける。

**(a) 原表（CACのPDF）そのものの誤り** ── 何もしない。値は原表のままが正しい。観察コードで拾えていなければ、本文で触れる箇所に書く。

**(b) 転記の誤り（PDFの字と台帳の値が違う）** ── 該当行に `corrections` を追記する。元の値は残す。

```json
"corrections": [
  {"date": "YYYY-MM-DD", "field": "entity", "as_printed": "<PDFの字のとおりの値>", "note": {"ja": "転記の誤り。原因：<折り返しの処理など>", "en": "Transcription error. Cause: ..."}}
]
```

あわせて、原因が `extract_attachment.py` にあるなら道具を直し、既に連結した全附件で同じ誤りが起きていないかを、全附件を再転記した結果と `registry.json` の差分で確かめる。差分のあった行すべてに `corrections` を追記する。コミット件名は `Correct F0123: <内容>`。

**(c) CACがPDFを差し替えた（ハッシュが変わった）** ── 既存の行は書き換えない。`sources` の該当項目の `observations` に、新しいファイルのハッシュ・取得日を `SOURCE_FILE_CHANGED` として追記し、新しいPDFを再転記した結果と既存の行の差分を、差分のあった行の `corrections` に記録する。

---

## 5. 失敗時の対応

`the-ai-forecast-registry` の `docs/UPDATE_RUNBOOK.md` 第5節と付録A〜Cを、そのまま適用する（コミットメッセージの誤り、署名の失敗、秘密鍵の混入、pushの拒否）。本書に固有の失敗は次の2つである。

- **`registry.json` の行を手で編集した。** `git checkout -- data/registry.json` で戻し、第1節または第4節の手順でやり直す
- **生成スクリプトを実行せずにCSVだけを直した。** `python scripts/build_registry.py` を実行し、生成されたCSVでコミットする

---

## 付録：v1.3（2026年11月22日）での実施の記録

- 附件1〜12のPDFは、著者が2026年8月28日にCACのハブページから取得し、Googleドライブに保存していたものを使った。附件13・14は、著者が2026年11月22日に取得した。各ファイルのSHA-256は `data/sources.csv` にある
- 転記と連結は、AIエージェント（Claude）がこの手順書の第1節の道具で行った。附件ごとに、序号が欠番・重複なく続くこと、公告本文の件数（記録のある附件11〜14。新規・累計・内訳）と行数が一致することをスクリプトで確かめた
- 附件13から、端末側の備案の表が、附件14から、擬人化された対話の備案の表と備案の変更の表が加わった。`DATA_SPEC.md` 第2節の原則で、それぞれを別の表として定義した。附件14の備案の変更1行（可灵、単位の名称の変更）は、元の備案の行（F0218）を書き換えず、C0001として記録した
- 2026年9月23日の別公告の端末側3件は、附件14の端末側の備案の表に序号8〜10として載った
- データと照合して、本文の3か所の件数を（2026年11月22日訂正）で訂正した。属地「国资委」の備案（11件→16件・15法人。附件10・11の4件が漏れていた）、上海汉枢科技のLongCat（5件→4件。序号202は別法人）、小米科技有限责任公司の備案（3件→6件）。第4章の属地の分布（序号189〜611の423件）は、データと全行一致した
- 表の判定を表題に基づく方式に改めた後、附件1〜12を再転記し、前の方式の結果と全行が一致することを確かめた
- 本文が序号を挙げている行（序号2・20・152・625・673・674・685・823・825・843・877・908・912・979・980、登記539・569・584）は、台帳の値と本文の記述が一致した
- 本文が第1章で開示した原表の問題（附件1の序号107〜112の並び、附件5の序号340〜345の列ずれ、附件6の序号414の「司」）は、すべて観察コードで拾えた。このほかに、附件6の序号368の「司」、備案184と登記26の番号の接頭辞、番号の内部の空白（備案8行・登記1行）を観察として記録した
- 著者の抜き取り確認は、コミットの前に行う
