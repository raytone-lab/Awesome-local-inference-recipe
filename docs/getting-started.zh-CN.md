# 入门指南

[English](getting-started.md) | **简体中文** | [日本語](getting-started.ja.md)

如何按预算和硬件挑选配方，并把它跑起来。

## 1. 按手头硬件挑选
| 你的硬件 | 从哪里开始 | 常用引擎 |
|---|---|---|
| Mac（Apple 芯片，统一内存 ≥32 GB） | 看 Mac 配方，内存越大可跑的模型越大 | MLX、oMLX、llama.cpp、mlx-serve |
| NVIDIA 消费级显卡（RTX 3090/4090/5090 等） | 量化后能放进显存的模型，或带卸载的 MoE 模型 | llama.cpp、vLLM、SGLang、ExLlama、Strata |
| DGX Spark | 128 GB 统一内存，适合大型 MoE | vLLM、TensorFold、ExLlama |
| AMD（Strix Halo、Radeon） | Strix Halo 可在统一内存里跑大模型 | llama.cpp（HIP/Vulkan）、Strata、Halogen |
| 二手数据中心卡（V100 等） | 每美元显存便宜，注意驱动和 CUDA 支持 | llama.cpp、Strata |

准备买硬件？参考 [README](../README.zh-CN.md) 的预算档位（2.5k / 7k / 14k / 30k 美元以内）。

## 2. 看懂一条配方
每一行是「模型 × 引擎 × 硬件 → 数字」。先看**来源等级**：✅ 实测、🏛️ 官方比 🔁 转述、📣 宣称更可靠。在 [配方库](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html) 里可按硬件、模型系列、引擎和标签（如 `4bit`、`MoE`）筛选。

## 3. 跑起来
1. 有 [指南页](../recipes/README.zh-CN.md) 的先看指南页，否则看来源链接。
2. 下载配方里写明的模型文件和量化版本（一般在 Hugging Face）。
3. 安装配方里写明的引擎版本，用到分支版（fork）会单独注明。
4. 启动命令以来源为准。标注「未公开」的请按原帖操作，不要猜参数。
5. 对比速度时，保持与来源相同的上下文长度和提示长度。

## 4. 分享你的结果
提交配方 issue 或 PR，详见 [贡献指南](../CONTRIBUTING.md)。
