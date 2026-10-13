# 信息源评估（2026-10-13 SGT 实测）

| 排名 | 来源 | 角色 | 给什么 | 自动化（实测） | 注意 |
|---|---|---|---|---|---|
| 1 | X | 主源（现状） | 实测 tok/s、硬件、热度 | 已在用 | 转述多，需回原帖 |
| 2 | Hugging Face 模型卡 | 主源 | 量化作者自带 benchmark 表（prompt/decode t/s） | ✅ `/api/models?sort=trendingScore&filter=gguf` 可用；`/raw/main/README.md` 可抓 | 卡上常不写硬件；只引用+链接 |
| 3 | r/LocalLLaMA | 主源 | 最多的消费级实测帖 | ❌ 匿名 `.json` 返回 HTML 拦截页；需 OAuth 应用（免费额度，ToS 禁止转售/训练） | 必须人工复核 |
| 4 | GitHub（llama.cpp discussions/releases、引擎 repo） | 主源（结构化） | 官方 bench 讨论串、release 性能说明 | GitHub API/GraphQL，需 token | 未本次测试 discussions |
| 5 | llamabench.ai / LocalScore / llamaperf | 交叉校验 | 带命令的跑分 | 需看各自导出/ToS | 不整库搬运，链接+对比 |
| 6 | Hacker News | 发现流 | 新引擎/项目发布 | ✅ Algolia API 可用（需 numericFilters 限时间） | 实测数字少 |
| 7 | arXiv | 发现流（方法） | 投机解码/量化新方法 | ⚠️ API 本次返回 429/空，需限速（≥3 秒/次）+重试 | 论文数字多为机房 GPU，不入配方表 |
| 8 | HF Spaces 榜单 | 参考 | 质量榜（非速度） | ✅ `/api/spaces?search=leaderboard` | 与 tok/s 无关 |
| 9 | 博客（MacStories 等） | 人工补充 | Mac 实测 | RSS | 低频 |
| 10 | Product Hunt | 跳过/月度看看 | 产品发布，几乎无性能数据 | GraphQL v2 需 token，商用要授权 | 噪声高 |
| 11 | Discord | 跳过 | 信息多但封闭 | 无合规 API 抓取 | ToS 禁止爬取 |

## 样本发现
- HF：[ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF)（下载 ~467 万）：llama.cpp、55 条 prompt，Q2_0 decode 93.79 t/s / prefill 367.49，IQ2_XS 70.30 / 108.19。硬件卡片片段中未见 → 待补。
- HF 趋势 GGUF 还有 [Venastine-Research/Xing4.0-29B-A4B-GGUF](https://huggingface.co/Venastine-Research/Xing4.0-29B-A4B-GGUF)、[nerkyor/...-MTP-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2)（名字堆砌，疑似刷榜，示范噪声）。
- HN：[Show HN: 在 M 系列 Mac 上 2GB 内存跑 Gemma 4 26B](https://news.ycombinator.com/item?id=49098510)（919 分，2026-07-29）；[Launch HN: Magnitude 自优化推理引擎](https://news.ycombinator.com/item?id=49911995)（194 分，2026-09-30）。
- Reddit：本次未拉到（被拦），无样本。arXiv：本次被限流，无样本。

## 建议管线
- 每日自动：HF trending GGUF/MLX → 抓 README 中含 t/s 的表 → 候选队列；HN Algolia（points>50）→ 发现队列。
- 每周：X 搜索（现有）+ Reddit（OAuth 后）top/week → 候选；arXiv 关键词（speculative decoding, quantization, KV cache, MoE offloading）→ 方法/引擎雷达，不直接入表。
- 全部候选人工复核：补硬件、引擎版本、命令，打来源等级后才入库。只存链接+摘要+数字。

## HF 自动抓取（scripts/ingest_hf.py）
- `python3 scripts/ingest_hf.py --limit 40 [--libs gguf,mlx --sorts trendingScore,downloads --delay 1]`，可选 `HF_TOKEN`。
- 输出 `data/candidates/hf-YYYY-MM-DD.json`，**不写** recipes.json；按 source_url / 历史候选去重；过滤 merge 堆名、uncensored 等噪声及无测速卡。
- 默认 source_level=宣称；`tok_s` 为卡内**最大**生成数，常混入其他硬件/模型/对比行，务必看 `raw_snippet` 与 `gen_tok_s_all`。
- 审核：`python3 scripts/review_candidates.py list | show <id> | approve <id> | reject <id> 原因`。approve 逐字段提示（回车保留、`-` 置空），hardware 与 tok_s 必填。
