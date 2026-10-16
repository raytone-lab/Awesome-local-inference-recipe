# Qwen3.6-35B-A3B-Escha-W2 · SGLang · RTX 5090 32GB

[English](hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.md) | **简体中文** | [日本語](hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.ja.md) · [← 返回列表](../README.zh-CN.md)

> 来源等级: **📣 宣称** · 日期: 2026-07-22 · 数字均摘自来源，未经本仓库复测。

## 硬件

- RTX 5090 32GB (NVIDIA 消费级)
- 参考价格: 仅显卡 $5,400 起（2026-10-11 最低追踪街价，MSRP $1,999，见 prices.json）

## 模型

- Qwen3.6-35B-A3B-Escha-W2 · `Escha W2（INT8=on）`
- 下载: [huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)

## 引擎

- SGLang — 安装见 https://github.com/sgl-project/sglang
- 备注: SGLang（sglang/serve.sh）

## 启动命令

```bash
MEM=0.78 CTXLEN=32768 bash sglang/serve.sh（5090 加 INT8=on ATTN_BACKEND=triton MEM=0.82）
```

## 关键参数

- 上下文: 32K（16GB 卡 8K×16）
- 并发: 单路 283；bs32 约 2,670（峰值 3,017.6 @32 流）
- 标签: `2bit`, `8bit`, `MoE`

## 预期速度

- 283 tok/s 生成 (📣 宣称)

## 注意事项

- 非一手实测（宣称/转述），实际速度可能不同。
- HF 模型卡（作者自报）; 每行均在对应实体卡上用卡内命令测得; 4090 temperature 0 vs 0.6：218 vs 102 tok/s，温度影响大
- 速度随驱动、引擎版本、上下文长度和提示长度变化。

## 来源与致谢

- [https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- 版权归原作者；本页仅摘要并链接。数据以 CC BY 4.0 发布。
