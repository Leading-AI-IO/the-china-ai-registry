# The China AI Registry

**988の名簿 ── 中国AIモデルを、当局の台帳から読む** <br/>
**The China AI Registry — Reading Chinese AI from the State's Own Ledger.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Language](https://img.shields.io/badge/Language-Japanese%20%7C%20English-blue)](docs/)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--08--28-brightgreen)](https://github.com/Leading-AI-IO/the-china-ai-registry/releases)

<p align="left">
  <img src="./assets/ogp_design.png" width="80%">
</p>

*Read this in other languages: [English](README_en.md)*

---

> **定義｜What is The China AI Registry**
>
> **本書とは**、山内怜史（Satoshi Yamauchi）による、中国のAI産業を当局の登録
> 名簿を母集団として構造化した分析である。中国では生成AIサービスの提供に
> 当局への備案（登録）が要る。2026年6月30日時点で備案済みサービスは988件、
> 登記済みアプリケーションは598件であり、個社名入りの名簿が2ヶ月ごとに
> 公表されている。規制のために作られた記録だが、結果として**生成AIの社会実装を
> 全数で追跡できる公的記録**になっている。米国・EU・日本には、本調査の範囲で
> これに対応するものを確認できなかった。名簿には製鉄所の転炉制御、
> 鉱山の安全生産管理、水道局のコールセンター、市民ホットライン、褥瘡管理、
> 災害対応が並び、テスラ上海・IKEA・シーメンス・BMW・コカ・コーラ・ASUSの
> 外資6社も同じ形式で登録されている。本書は988件を業種別に整理し、読者が
> 自業界の実装事例を社名とモデル名のレベルで引ける形にする。あわせて、
> 上場したAIラボの監査済み決算から、**計算資源のコストが売上原価とR&D費用に
> 分かれて計上される構造**を読む。中心命題：**この産業は、企業では数えられて
> いない。名簿で数えられている。**
>
> **This book** is a structural analysis by Satoshi Yamauchi that uses China's
> official generative-AI filing registry as its population. As of 30 June 2026,
> 988 services and 598 applications are registered, and the named lists are
> published every two months. The ten or so companies discussed abroad are a
> fraction of that. The rest includes steel-converter control, a water utility's
> call centre, a municipal hotline, and a Lao-language foundation model —
> alongside Tesla Shanghai, IKEA, Siemens, BMW and Coca-Cola. Eleven central
> state-owned enterprises appear under a jurisdiction code rather than a
> province. The five Chinese AI models you can name are under 1% of the ones
> China counts. The industry is not counted by companies — it is counted by a
> registry, and the registry is public.
>
> **利害関係の開示 / Disclosure**：著者は中国の政府機関、AI企業、半導体企業の
> いずれとも取引関係を持たず、いずれからも資金提供を受けていない。本書は
> 独立分析である。中国政府の公告は中国側が自国の制度をどう設計したかの表明
> として扱い、上場企業の決算は企業側の説明として扱う。どちらも中立の記述と
> しては扱わない。The author has no commercial relationship with any Chinese
> government agency, AI company, or semiconductor firm, and receives no funding
> from any of them. Government notices are treated as the state's own account of
> its system, and audited filings as the companies' own account of themselves —
> neither as neutral description.
>
> *著者・全書籍一覧 / Author & full catalog: [github.com/Leading-AI-IO](https://github.com/Leading-AI-IO)*

---

## 📖 概要

DeepSeek。Qwen。Kimi。GLM。MiniMax。日本語圏で「中国のAIモデル」が語られるとき、現れる名前はおおむねこの5つに収まる。ベンチマークのスコアとAPI価格を横に並べた比較表が作られ、そこで議論が終わる。この5社は実在するし、表の数字も正しい。

**問題は分母である。この5社は、中国のAI産業の何割を占めるのか。**

表を作った側も、読んだ側も、この問いに答えられない。分母を知らないまま、分子だけを比べている。中国は不透明だから仕方ない——そう説明されることが多い。だが分母は推計する必要がない。**中国当局が、個社名入りで公開している。**

中国では生成AIサービスの提供に当局への備案（登録）が要る。2026年6月30日時点で備案済みサービス**988件**、登記済みアプリケーション**598件**。個社名入りの名簿が**2ヶ月ごと**に公告され、2024年4月から2026年6月まで12回分が積み上がっている。規制のために作られた記録だが、結果として**生成AIの社会実装を全数で追跡できる公的記録**になっている。

そこに何があるか。**製鉄所の転炉制御**（河北永洋特鋼「転炉智能煉鋼大模型」）。**鉱山の安全生産管理**。**水道局のコールセンター**（北京市自来水集団「京水客服」）。**市民ホットライン**（北京市市民熱線服務中心「12345智能体」）。**褥瘡の管理支援**（江蘇省人民医院「舒圧伴・PressGuard」）。**災害対応**（応急管理部大数据中心「久安-知言」「久安-知図」）。石油・天然ガス管網・電力・航空・物流・アルミの基幹企業が、自前の大規模モデルを登録している。**対話アシスタントでも社内文書検索でもない。プロセスと公共サービスそのものである。**

外資も同じ名簿にいる。**テスラ上海**（序号843）、**IKEA中国**（序号825）、**シーメンス中国**（序号674）、**コカ・コーラ上海**（序号877）、**BMW中国**（序号912）、**ASUS上海**（序号823）。中国企業と同じ列構成で、通し番号で並んでいる。中国事業を持つ企業にとっては、そのまま先例の所在になる。

一方、日本語圏で語られる中国AIモデルは10社前後である。なぜその10社なのか。品質で選ばれたのではない。**海外からAPIで叩けるか、重みが配布されているか、英語の情報があるか**——この到達フィルタを通過したものだけが記事に現れ、通過しなかったものは存在ごと消える。**転炉も、水道も、褥瘡も、災害対応も、このフィルタを通過しない。** 社外に売っていないからである。

分類の基準も当局側にある。属地欄には省でも直轄市でもない **「国资委」** という区分があり、この行は備案番号が例外なく `ZhongYangQiYe-` で始まる。該当は全期間で11件。中国石油天然気集団（CNPC）、国家石油天然気管網集団（PipeChina）、中国電力科学研究院、中国電科集団（CETC）、中鋁集団（Chinalco）、国家能源集団。**日本で言えば、JERA・NTT・JR・日本郵船・日本軽金属が、それぞれ自社の大規模モデルを持ち、国に登録している状態である。**

順序にも通説とのずれがある。備案の起点は2023年8月31日で、同日に8件が並ぶ。百度、智譜、ByteDance、百川、**中国科学院自動化研究所**、MiniMax、SenseTime、**上海AI Lab**——国家研究機関が初日から入っている。一方、**DeepSeekは序号152、2024年5月13日である。** 智譜の76倍、Moonshotの9.5倍遅い。

そして開示では、通説が逆転している。**智譜（HKEX 2513）とMiniMax（HKEX 00100）は2026年1月に香港上場を果たし、監査済みの年度決算を公表している。** MiniMaxの2025年度は売上US$79.0百万（+158.9%）、粗利率25.4%、うち**73.0%が中国本土外**。最大の計算資源支出は売上原価ではなく**R&D費用（US$252.8百万・売上原価の4.3倍）**に計上されており、**粗利率25.4%は推論だけを見た数字である。** 自社でAIサービスの収支計画を立てるとき、この分離を知らずに他社の粗利率をベンチマークすると、必要な資金を大きく見誤る。同じことをOpenAI・Anthropicについて確認することはできない。両社とも非上場である。

**読者が持ち帰れるものは三つある。**（1）第4章で988件を業種別に整理し、**自業界の実装事例を社名とモデル名のレベルで引ける**形にする。（2）第8章で外資6社の備案から、**中国市場に出すときの実務の先例**を示す。（3）第6章で**AI事業の経済性を監査済みの実数で読む**。

中心命題は一つである。**この産業は、企業では数えられていない。名簿で数えられている。**

なお本書は、一次資料に到達できなかったものを扱わない。各モデルの技術的性能の比較、ベンチマークスコアの検証、多くの企業の学習チップ、iFlytek「星火」およびSenseTime「大装置」の計算基盤の販売形態、各モデルの日本語性能の独立測定——いずれも主題に関わるが、測定者・測定日・バージョンの三点が揃った公開データが存在しないか、企業側が公表していない。**到達できなかったものを、到達したかのように書かない。** また備案は「登録した」以上の意味を持たない。**名簿に載っている実装が成功しているかどうかを、本書は検証していない。**

---

## 📄 ドキュメント

| ファイル | 言語 | 内容 |
| --- | --- | --- |
| [the-china-ai-registry_JP.md](./docs/jp/the-china-ai-registry_JP.md) | 🇯🇵 日本語 | 本文（日本語版） |
| [the-china-ai-registry_EN.md](./docs/en/the-china-ai-registry_EN.md) | 🇺🇸 English | 本文（英語版） |

---

## 🔄 更新履歴

本書は**定点観測型**のOSS書籍である。対象が現在進行で動いているため、事実が動くたびに追記し、**以前の記述が当たったか外れたかを版として記録する。**

**本書の改訂周期は、著者の都合ではなく当局の公表周期に同期する。** CACは2ヶ月ごとに新しい附件を公告する。件数は増え、属地の分布は動き、新しい類型の登録者が現れる。本書はその都度、名簿に戻って数え直す。

| 版 | 日付 | 内容 |
| --- | --- | --- |
| **v1.0** | 2026-08-28 | 初版公開（備案 序号1〜988／登記 序号1〜598・附件1〜12 全数連結） |

---

## 📑 目次

- **序章:** この5社は、中国のAI産業の何割か
- **第1章:** 名簿の読み方 ── 当局が数えているもの
- **第2章:** 起点 ── 2023年8月31日の8件
- **第3章:** 認知の順と、登録の順は違う
- **第4章:** 実装のカタログ ── どの業務に、AIが入ったか
- **第5章:** 依存の方向 ── チップ・重み・国家
- **第6章:** 開示の非対称 ── 上場した中国、していない米国
- **第7章:** この産業を読むための四つの軸
- **第8章:** 日本の読者は、この名簿から何を学べるか
- **終章:** 名簿では分からないこと

---

## 🔗 Related Projects

本書は、以下のOSSプロジェクトと相互に接続されている。

| プロジェクト | 概要 | リンク |
| --- | --- | --- |
| **US-China AI Competition**         | 米中AI競争の多層構造。決めているのは強さではなく条件である | [GitHub](https://github.com/Leading-AI-IO/us-china-ai-competition)        |
| **Frontier-Grade Open Weights**     | フロンティア級のオープンウェイトモデルは、開かれたのか | [GitHub](https://github.com/Leading-AI-IO/frontier-grade-open-weights)    |
| **The AI Strategist**               | AIストラテジストという職業を定義し、BTC交差点で戦うための実践的フレームワーク | [GitHub](https://github.com/Leading-AI-IO/the-ai-strategist)              |
| **Depth & Velocity**                | 生成AI時代の新規事業開発方法論 | [GitHub](https://github.com/Leading-AI-IO/depth-and-velocity)             |
| **The Silence of Intelligence**     | Anthropic CEO ダリオ・アモディの思想を体系化。産業構造の解剖シリーズ第2弾 | [GitHub](https://github.com/Leading-AI-IO/the-silence-of-intelligence)    |
| **The Anatomy of Anthropic**        | Anthropicの戦略・製品・研究・安全性を包括的に解剖 | [GitHub](https://github.com/Leading-AI-IO/anatomy-of-anthropic)           |
| **The Palantir Impact**             | Palantir Foundryのオントロジー戦略を解剖。産業構造の解剖シリーズ第1弾 | [GitHub](https://github.com/Leading-AI-IO/palantir-ontology-strategy)     |
| **What They Won't Teach You**       | AIに有利な世代が教えない、AIの使い方と"思考のOS" | [GitHub](https://github.com/Leading-AI-IO/what-they-wont-teach-you)       |
| **The Edge of Intelligence**        | AIがあなたのデバイスで動く時代：クラウドの終わりと、エッジの始まり | [GitHub](https://github.com/Leading-AI-IO/edge-ai-intelligence)           |
| **The Redesign of Design Strategy** | デザイン戦略の再定義。IDEO崩壊の構造分析を含む | [GitHub](https://github.com/Leading-AI-IO/design-strategy-in-the-ai-era)  |
| **The Orchestrator**                | AI時代に最も希少な人材像「AIオーケストレーター」を定義 | [GitHub](https://github.com/Leading-AI-IO/the-orchestrator-in-the-ai-era) |
| **Advertising, Redesigned**         | AI時代の広告の未来を、7社の戦略と構造分析から描くOSS書籍 | [GitHub](https://github.com/Leading-AI-IO/advertising-redesigned)         |
| **The AI Organization**             | AI導入が失敗する本質は技術ではなく組織にある。AI時代の組織論 | [GitHub](https://github.com/Leading-AI-IO/the-ai-organization)            |
| **The Structural Shift from SaaS**  | SaaSからService-as-a-Softwareへの構造的転換。Next SaaS ビジネスモデル | [GitHub](https://github.com/Leading-AI-IO/saas-is-dead-the-next-ai-business-model) |
| **The 10:80:10 Principle**          | 人とAIの共創黄金比「10:80:10」の法則——AI時代の思考のOS | [GitHub](https://github.com/Leading-AI-IO/the-10-80-10-principle)         |
| **A Trillion Dollars and a Firebomb** | 1兆ドルと火炎瓶。AI時代の同時加速する現実 | [GitHub](https://github.com/Leading-AI-IO/a-trillion-and-a-firebomb)      |
| **The End of the Attention Economy** | アテンション・エコノミーの終わり。次世代SNSの在り方とは？ | [GitHub](https://github.com/Leading-AI-IO/the-attention-economy-is-over)  |
| **The Growth Engine of Anthropic**  | Anthropicの1兆ドル到達の構造解剖 | [GitHub](https://github.com/Leading-AI-IO/the-growth-engine-of-anthropic) |
| **The Agentic Commerce Economy**    | AIエージェントが購買を代行する時代、広告モデルの構造的変化 | [GitHub](https://github.com/Leading-AI-IO/agentic-commerce-economy)       |
| **Will AI Break the Planet**        | 数十兆円のインフラ投資と、地球温暖化の「不可逆ライン」 | [GitHub](https://github.com/Leading-AI-IO/will-ai-break-the-planet)       |
| **The Forward Deployed Shift**      | 成果実装 ── FDEが示す、AIで「作る」が終わった世界の価値のありか | [GitHub](https://github.com/Leading-AI-IO/the-forward-deployed-shift)     |
| **Earned AI Model Optionality**     | AIモデルは選べる。選べるのは、選べるようにした企業だけだ | [GitHub](https://github.com/Leading-AI-IO/earned-ai-model-optionality)    |

---

## 👤 著者

**Satoshi Yamauchi** (山内 怜史)

* **AI Strategist & Business Designer at Sun Asterisk Inc.**

* **Founder / AI Strategist at [Leading.AI](https://www.leading-ai.io/)**

* 15年以上にわたりBusiness・Technology・Creativeの3領域を越境。フューチャーアーキテクトでITコンサルタントとして40案件のPL/PMを推進後、リクルートで事業戦略・新規事業開発に従事。Sun Asteriskでビジネスデザイナー兼AIストラテジストとして、新規事業×生成AIの方法論「Depth & Velocity」を体系化。

* This project is part of the research by Leading.AI.

* [📒 Read my insights on Note](https://note.com/satoshi_yamauchi)

* [🌐 Visit Leading.AI Official Website](https://www.leading-ai.io/)

---

## 🤝 Contributing

Issues and Pull Requests are welcome. 本書の構造分析に対するフィードバック、CAC備案名簿の新規公告、上場企業の開示情報、一次資料の追加、誤字脱字の修正、翻訳へのContributeを歓迎します。

とくに、本書が「原典未到達」として本文から除外した以下の項目について、一次資料への到達経路をご存知の方からの情報提供を歓迎します。

- 智譜（HKEX 2513）2025年度決算の原本
- GLM-5.3のライセンスおよび重みの実配布状況
- 各社の学習に用いられたチップ
- iFlytek「星火」・SenseTime「大装置」の計算基盤の販売形態と導入規模

---

## 📝 License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).<br>
© 2026 Satoshi Yamauchi / [Leading AI](https://www.leading-ai.io/) — Licensed under CC BY 4.0
