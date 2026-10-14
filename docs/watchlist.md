# Recipe sources to watch / 重点跟踪来源

Generated from `data/sources.json` (2026-10-14). Tier A = 参数具体且可复现；B = 有具体数字但条件不全；C = 多为转述或覆盖面窄。

| Tier | Name | Platform | Followers | Focus | Why | Sample |
|---|---|---|---|---|---|---|
| A | [MiaAI_lab](https://x.com/MiaAI_lab) | X | 40561 | DGX Spark 1–4 台 / RTX 5090 / RTX PRO 6000；vLLM · SGLang · TensorFold · EXL3 | 每个 recipe 有 GitHub 仓库 + 启动脚本 + sparkDash 按流数基准，社区多人复现（误差 ≤8%） | [link](https://x.com/MiaAI_lab/status/2105598458547646875) |
| A | [mia-ai.net](https://mia-ai.net/models) | Web | — | Mia 的 23 个 recipe 汇总（含 GitHub 星数、单流/多流/预填充/上下文） | 结构化数字，最适合定期抓取 | [link](https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold) |
| A | [coldniko](https://x.com/coldniko) | X | 7647 | Strata 引擎作者（GitHub Niko1221/Strata）；消费级 GPU + 内存卸载、V100/MI50 老卡 | 引擎一手发布与参数说明；回复里常给具体并行/卸载设置 | [link](https://x.com/coldniko/status/2109014509063139413) |
| A | [Niko1221/Strata](https://github.com/Niko1221/Strata) | GitHub | — | Strata 引擎 README / docs/OLDER_GPUS.md | 官方基准表，repo 已有 29 条 Strata 数据 | [link](https://github.com/Niko1221/Strata) |
| A | [0xSero](https://x.com/0xSero) | X | 74813 | DGX Spark 多机 / RTX 3090 + NVMe 卸载 / Intel Arc | 发布带 KLD、top-token 一致率、KV 池大小的完整 recipe，互动最高（2.4k 赞） | [link](https://x.com/0xSero/status/2106373861818224907) |
| A | [ashxhart](https://x.com/ashxhart) | X | 8346 | Mac Studio M3 Ultra、DGX Spark；oMLX PR、TensorFold 贡献者 | 给上下文长度、未缓存 PP 等条件，且向引擎提 PR | [link](https://x.com/ashxhart/status/2099219170546028647) |
| A | [WescheNex1q](https://x.com/WescheNex1q) | X | 3142 | Mac Studio M4 Max vs DGX Spark | 受控对比：同 GGUF sha256、分项 prose/code/json、TTFT | [link](https://x.com/WescheNex1q/status/2103651224650207607) |
| A | [niklaslenz_ai](https://x.com/niklaslenz_ai) | X | 721 | RTX 5090、2×5060 Ti、4×DGX Spark | 独立复现他人 recipe 并公布原始文件，30+ 组合矩阵 | [link](https://x.com/niklaslenz_ai/status/2105623763018453099) |
| B | [JASONMCNAB](https://x.com/JASONMCNAB) | X | 907 | DGX Spark (GB10) | 逐流数复现 Mia recipe 并列出对照值 | [link](https://x.com/JASONMCNAB/status/2101367210404966460) |
| B | [sudoingX](https://x.com/sudoingX) | X | 37633 | 各显存档 GPU（6GB→256GB 双 Spark） | 按显存档整理的 bench book，覆盖面广；单条细节较少 | [link](https://x.com/sudoingX/status/2095300994259100009) |
| B | [yume_arasaki](https://x.com/yume_arasaki) | X | 2481 | DGX Spark、汇总长帖 | 已是 repo 最大来源（42 条），长帖汇总他人数字，需回溯原帖 | [link](https://x.com/yume_arasaki/status/2106837882870886438) |
| B | [TeksEdge](https://x.com/TeksEdge) | X | 11801 | Strix Halo / DGX Spark；llama.cpp PR 与 fork | 第一时间转述 llama.cpp 新 PR/fork 的速度，多为转述 | [link](https://x.com/TeksEdge/status/2092673436904489362) |
| B | [jundotkim](https://x.com/jundotkim) | X | 3954 | oMLX 作者（Hugging Face） | 引擎 release note，适合追踪版本差异 | [link](https://x.com/jundotkim/status/2103220348263227765) |
| B | [ivanfioravanti](https://x.com/ivanfioravanti) | X | 43683 | Apple MLX | MLX 生态大号，Mac 新机/新模型首测 | [link](https://x.com/ivanfioravanti) |
| B | [CryptoBandit100](https://x.com/CryptoBandit100) | X | 628 | 3×DGX Spark + Mac Studio | 写清 KV 量化、MTP K、temp、引擎版本 | [link](https://x.com/CryptoBandit100/status/2106374669477761493) |
| C | [Oluwaphilemon1](https://x.com/Oluwaphilemon1) | X | 9689 | Mac vs Spark 对比 | 多为整理/转述 WescheNex1q 等数据 | [link](https://x.com/Oluwaphilemon1/status/2091693026087182378) |
| C | [hnakamur2](https://x.com/hnakamur2) | X | 1497 | 2× ThinkStation PGX（Spark OEM） | 日文复现 Mia recipe，含 TTFT | [link](https://x.com/hnakamur2/status/2090784021630566613) |
| C | [llm_frontier_jp](https://x.com/llm_frontier_jp) | X | 477 | GPU/Mac 本地 LLM（日文） | 区分自测与引用的 Spark 对比整理 | [link](https://x.com/llm_frontier_jp/status/2108048696906825765) |
| C | [aartiles24](https://x.com/aartiles24) | X | 6495 | MacBook M5 Pro | TensorFold vs mlx-serve vs oMLX 同机倍率 | [link](https://x.com/aartiles24/status/2104179801388884125) |
| C | [Urthoo](https://x.com/Urthoo) | X | 918 | 2× DGX Spark | vLLM→TensorFold 前后对照（1/3 流、预填充） | [link](https://x.com/Urthoo/status/2106426248759005362) |
| C | [redp314](https://x.com/redp314) | X | 2081 | MacBook M3 Max | 固定提示/温度的引擎对比板 | [link](https://x.com/redp314/status/2093588456396210479) |
| C | [iam_agg](https://x.com/iam_agg) | X | 2503 | Mac Studio M5 Ultra 256GB | M5 Ultra 多引擎早期数据 | [link](https://x.com/iam_agg/status/2104413091996008624) |
| C | [AlicanKiraz0](https://x.com/AlicanKiraz0) | X | 39318 | 4× DGX Spark（土耳其语） | 多机 NVFP4 + DFlash2 配置 | [link](https://x.com/AlicanKiraz0/status/2093843767866405145) |
