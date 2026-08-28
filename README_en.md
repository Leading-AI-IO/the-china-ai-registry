# The China AI Registry

"The five Chinese AI models you can name are under 1% of the ones China counts." 

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Language](https://img.shields.io/badge/Language-Japanese%20%7C%20English-blue)](docs/)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--08--28-brightgreen)](https://github.com/Leading-AI-IO/the-china-ai-registry/releases)

<p align="left">
  <img src="./assets/ogp_design.png" width="80%">
</p>

*Read this in other languages: [日本語](README.md)*

---

> **Definition**
>
> **This book** is a structural analysis by Satoshi Yamauchi (山内怜史), AI
> Strategist, that uses China's official generative-AI filing registry as its
> population. Providing a generative AI service in China requires filing with
> the authorities. As of 30 June 2026, 988 services and 598 applications are
> filed, and the named lists are published every two months. The registry was
> created to manage expression, not to promote industry — yet the result is a
> public record that tracks the social deployment of generative AI in full. For
> the United States, the EU and Japan, this book was unable to confirm a
> corresponding record. On the list are converter control in a steel mill, mine
> safety management, a water utility's call centre, a municipal hotline,
> pressure-ulcer management and disaster response — alongside Tesla Shanghai,
> IKEA, Siemens, BMW, Coca-Cola and ASUS, filed in the same format. Eleven
> central state-owned enterprises appear under a supervisory jurisdiction code
> rather than a province, identified by the filing-number prefix
> `ZhongYangQiYe-`. The book organises the 988 by industry so a reader can look
> up deployment cases in their own sector at the level of company and model
> name, and reads the audited annual results of listed AI labs to show how **the
> cost of compute is split across cost of sales and R&D expenses**. The five
> Chinese AI models you can name are under 1% of the ones China counts. The
> industry is not counted by companies — it is counted by a registry, and the
> registry is public.
>
> **Disclosure**: The author has no commercial relationship with any Chinese
> government agency, AI company, or semiconductor firm, and receives no funding
> from any of them. This is independent analysis. Government notices are treated
> as the state's own account of its system, and audited filings as the
> companies' own account of themselves — neither as neutral description.
>
> *Author & full catalog: [github.com/Leading-AI-IO](https://github.com/Leading-AI-IO)*

---

## 📖 Overview

DeepSeek. Qwen. Kimi. GLM. MiniMax. When Chinese AI models are discussed outside China, the names that appear tend to fall within these five. A comparison table is built, benchmark scores and API prices lined up side by side, and the discussion ends there. These five companies are real, and the figures in that table are correct.

**The problem is the denominator. What fraction of China's AI industry do these five represent?**

Neither the person who built the table nor the person who read it can answer. The denominator is unknown; only the numerators are being compared. China is opaque, so nothing can be done — that is the usual explanation. But the denominator does not have to be estimated. **Chinese authorities publish it, with company names attached.**

Providing a generative AI service in China requires filing with the authorities. As of 30 June 2026, **988 services** and **598 applications** had completed filing and registration. The named lists are published **every two months**, and twelve sets of attachments covering April 2024 through June 2026 have accumulated. The registry was created for regulatory purposes, yet the result is **a public record that tracks the social deployment of generative AI in full**.

What is on it? **Converter control in a steel mill** (Hebei Yongyang Special Steel). **Mine safety management**. **A water utility's call centre** (Beijing Waterworks Group). **A municipal hotline** (the Beijing Citizen Hotline Service Center's "12345 agent"). **Pressure-ulcer management** (Jiangsu Province Hospital's "PressGuard"). **Disaster response** (two filings by the Big Data Center of the Ministry of Emergency Management). Backbone enterprises in oil, gas pipelines, electric power, aviation, logistics and aluminium have filed their own large models. **Not a conversational assistant, and not internal document search — processes and public services themselves.**

Foreign companies are on the same list. **Tesla Shanghai** (No. 843), **IKEA China** (No. 825), **Siemens China** (No. 674), **Coca-Cola Shanghai** (No. 877), **BMW China** (No. 912), **ASUS Shanghai** (No. 823) — in the same column structure, in the same running sequence as Chinese firms. For companies with China operations, this is directly a body of precedent.

So why do only ten or so companies appear in the articles? Not because of quality. **Can it be called from abroad through an API, are the weights distributed, is there material in English** — only what passes this reachability filter appears, and what does not disappears from the article altogether. **Converter control, the water utility, PressGuard and disaster response all fail this filter,** because they are not being sold outside the organisation.

The basis of classification also sits on the authorities' side. The jurisdiction column holds one entry that is not geographic: **国资委**, the State-owned Assets Supervision and Administration Commission. Rows carrying it have filing numbers beginning, without exception, with `ZhongYangQiYe-`. Twelve such filings span eleven enterprises: CNPC, PipeChina, the China Electric Power Research Institute, CETC, Chinalco, China Energy Investment Corporation and others.

The ordering also runs against the common account. Filing begins on 31 August 2023 with eight entries on the same day: Baidu, Zhipu, ByteDance, Baichuan, **the Institute of Automation of the Chinese Academy of Sciences**, MiniMax, SenseTime and **Shanghai AI Lab** — a national research institute is in from day one. **DeepSeek, meanwhile, is No. 152, filed 13 May 2024** — 76 times later than Zhipu and 9.5 times later than Moonshot.

And on disclosure, the common account is inverted. **Zhipu (HKEX 2513) and MiniMax (HKEX 00100) listed in Hong Kong in January 2026 and publish audited annual results.** MiniMax's fiscal 2025 shows revenue of US$79.0m (+158.9%), a 25.4% gross margin, and **73.0% of revenue from outside mainland China**. The largest compute spend is recorded not in cost of sales but in **R&D expenses (US$252.8m, 4.3 times cost of sales)** — so **the 25.4% gross margin looks only at inference**. Benchmark another company's gross margin without knowing about this split and you will badly understate the capital your own AI service requires. The same cannot be confirmed for OpenAI or Anthropic. Both are private.

**There are three things a reader can take away.** (1) Chapter 4 organises the 988 by industry so you can **look up deployment cases in your own sector at the level of company and model name**. (2) Chapter 8 draws **precedents for entering the Chinese market** from the six foreign subsidiaries. (3) Chapter 6 **reads the economics of an AI business in audited real figures**.

The central proposition is one. **This industry is not counted by companies. It is counted by a registry.**

This book does not treat what it could not reach in primary sources. Comparison of technical performance, verification of benchmark scores, the training chips used by most companies, the sales model behind iFlytek's "Spark" and SenseTime's "SenseCore," independent measurement of Japanese-language performance — all bear on the subject, but either no public data exists with all three of measurer, measurement date and version, or the companies have not disclosed it. **What could not be reached is not written as though it had been.** A filing, moreover, means nothing beyond "this was filed." **Whether the deployments on the registry are succeeding has not been verified by this book.**

---

## 📄 Document

| File | Language | Contents |
| --- | --- | --- |
| [the-china-ai-registry_JP.md](./docs/jp/the-china-ai-registry_JP.md) | 🇯🇵 日本語 | Full text (Japanese) |
| [the-china-ai-registry_EN.md](./docs/en/the-china-ai-registry_EN.md) | 🇺🇸 English | Full text (English) |

---

## 🔄 Update History

This is a **living document**. Because the subject is in motion, entries are appended as facts change, and **whether earlier statements held or failed is recorded as a version**.

**This book's revision cycle synchronises with the authorities' publication cycle, not the author's convenience.** The CAC publishes a new attachment every two months. Counts rise, the jurisdiction distribution shifts, and new categories of filer appear. Each time, this book returns to the registry and counts again.

Note that the opening line ("under 1%") requires no update as the denominator grows. Filings are cumulative and do not decrease, so the statement can only become stronger as the denominator rises. **Precise absolute figures are carried by the body; the update-free summary is carried by the opening.**

| Version | Date | Contents |
| --- | --- | --- |
| **v1.0** | 2026-08-28 | Initial release (filings Nos. 1–988 / registrations Nos. 1–598; Attachments 1–12 fully joined) |

---

## 📑 Table of Contents

- **Prologue:** What Fraction of China's AI Industry Are These Five?
- **Chapter 1:** How to Read the Registry ── What the Authorities Are Counting
- **Chapter 2:** The Starting Point ── Eight Entries on August 31, 2023
- **Chapter 3:** Recognition Order and Filing Order Do Not Coincide
- **Chapter 4:** A Catalogue of Deployments ── Which Lines of Work AI Entered
- **Chapter 5:** The Direction of Dependence ── Chips, Weights, and the State
- **Chapter 6:** The Asymmetry of Disclosure ── China Listed, America Not
- **Chapter 7:** Four Axes for Reading This Industry
- **Chapter 8:** What Readers Outside China Can Learn From This Registry
- **Epilogue:** What the Registry Cannot Show

---

## 🔗 Related Projects

This book is cross-connected with the following open-source projects.

| Project | Summary | Link |
| --- | --- | --- |
| **US-China AI Competition**         | The layers of US-China AI competition. What is decided is not who is stronger, but the terms | [GitHub](https://github.com/Leading-AI-IO/us-china-ai-competition)        |
| **Frontier-Grade Open Weights**     | Were frontier-grade open-weight models actually opened | [GitHub](https://github.com/Leading-AI-IO/frontier-grade-open-weights)    |
| **The AI Strategist**               | Defining the AI Strategist as a profession, and a practical framework for the BTC intersection | [GitHub](https://github.com/Leading-AI-IO/the-ai-strategist)              |
| **Depth & Velocity**                | A methodology for new business development in the generative AI era | [GitHub](https://github.com/Leading-AI-IO/depth-and-velocity)             |
| **The Silence of Intelligence**     | Systematising the thought of Anthropic CEO Dario Amodei. Industry anatomy series, part 2 | [GitHub](https://github.com/Leading-AI-IO/the-silence-of-intelligence)    |
| **The Anatomy of Anthropic**        | A comprehensive dissection of Anthropic's strategy, products, research and safety | [GitHub](https://github.com/Leading-AI-IO/anatomy-of-anthropic)           |
| **The Palantir Impact**             | Dissecting Palantir Foundry's ontology strategy. Industry anatomy series, part 1 | [GitHub](https://github.com/Leading-AI-IO/palantir-ontology-strategy)     |
| **What They Won't Teach You**       | The use of AI, and the "OS for thinking," that the AI-advantaged generation will not teach you | [GitHub](https://github.com/Leading-AI-IO/what-they-wont-teach-you)       |
| **The Edge of Intelligence**        | When AI runs on your device: the end of cloud, the beginning of edge | [GitHub](https://github.com/Leading-AI-IO/edge-ai-intelligence)           |
| **The Redesign of Design Strategy** | Redefining design strategy, including a structural analysis of IDEO's collapse | [GitHub](https://github.com/Leading-AI-IO/design-strategy-in-the-ai-era)  |
| **The Orchestrator**                | Defining the scarcest talent profile of the AI era: the AI Orchestrator | [GitHub](https://github.com/Leading-AI-IO/the-orchestrator-in-the-ai-era) |
| **Advertising, Redesigned**         | The future of advertising in the AI era, drawn from seven companies' strategies | [GitHub](https://github.com/Leading-AI-IO/advertising-redesigned)         |
| **The AI Organization**             | Why AI adoption fails is organisational, not technical. Organisation theory for the AI era | [GitHub](https://github.com/Leading-AI-IO/the-ai-organization)            |
| **The Structural Shift from SaaS**  | The structural shift from SaaS to Service-as-a-Software | [GitHub](https://github.com/Leading-AI-IO/saas-is-dead-the-next-ai-business-model) |
| **The 10:80:10 Principle**          | The golden ratio of human-AI co-creation — an OS for thinking in the AI era | [GitHub](https://github.com/Leading-AI-IO/the-10-80-10-principle)         |
| **A Trillion Dollars and a Firebomb** | A trillion dollars and a firebomb. Realities accelerating simultaneously in the AI era | [GitHub](https://github.com/Leading-AI-IO/a-trillion-and-a-firebomb)      |
| **The End of the Attention Economy** | The end of the attention economy. What should the next generation of social platforms be | [GitHub](https://github.com/Leading-AI-IO/the-attention-economy-is-over)  |
| **The Growth Engine of Anthropic**  | A structural anatomy of Anthropic's path to a trillion dollars | [GitHub](https://github.com/Leading-AI-IO/the-growth-engine-of-anthropic) |
| **The Agentic Commerce Economy**    | When AI agents transact on your behalf: the structural change in advertising models | [GitHub](https://github.com/Leading-AI-IO/agentic-commerce-economy)       |
| **Will AI Break the Planet**        | Tens of trillions in infrastructure investment, and the irreversible line of global warming | [GitHub](https://github.com/Leading-AI-IO/will-ai-break-the-planet)       |
| **The Forward Deployed Shift**      | Outcome implementation — where value sits once AI has ended "building" | [GitHub](https://github.com/Leading-AI-IO/the-forward-deployed-shift)     |
| **Earned AI Model Optionality**     | AI models can be chosen. Only companies that built for it get to choose | [GitHub](https://github.com/Leading-AI-IO/earned-ai-model-optionality)    |

---

## 👤 Author

**Satoshi Yamauchi** (山内 怜史)

* **AI Strategist & Business Designer at Sun Asterisk Inc.**

* **Founder / AI Strategist at [Leading.AI](https://www.leading-ai.io/)**

* For over fifteen years, working across the three domains of Business, Technology and Creative. After leading forty engagements as PL/PM as an IT consultant at Future Architect, he moved to Recruit to work on business strategy and new business development. At Sun Asterisk, as Business Designer and AI Strategist, he systematised "Depth & Velocity," a methodology for new business development with generative AI.

* This project is part of the research by Leading.AI.

* [📒 Read my insights on Note](https://note.com/satoshi_yamauchi)

* [🌐 Visit Leading.AI Official Website](https://www.leading-ai.io/)

---

## 🤝 Contributing

Issues and Pull Requests are welcome. Feedback on the structural analysis, newly published CAC filing notices, disclosure from listed companies, additional primary sources, corrections to typographical errors, and contributions to translation are all appreciated.

In particular, information is welcome from anyone who knows a route to the primary sources this book excluded from the body as unreached.

- The original fiscal 2025 financial statements of Zhipu (HKEX 2513)
- The licence and actual weight-distribution status of GLM-5.3
- The chips used for training at each company
- The sales model and deployment scale of the compute platforms behind iFlytek's "Spark" and SenseTime's "SenseCore"

---

## 📝 License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).<br>
© 2026 Satoshi Yamauchi / [Leading AI](https://www.leading-ai.io/) — Licensed under CC BY 4.0
