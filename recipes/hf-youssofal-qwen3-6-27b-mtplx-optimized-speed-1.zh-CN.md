# Qwen3.6-27B-MTPLX-Optimized-Speed · MTPLX · MacBook M5 Max

[English](hf-youssofal-qwen3-6-27b-mtplx-optimized-speed-1.md) | [简体中文](hf-youssofal-qwen3-6-27b-mtplx-optimized-speed-1.zh-CN.md) · [← 返回列表](../README.zh-CN.md)

> 来源等级: **📣 宣称** · 日期: 2026-05-03 · 数字均摘自来源，未经本仓库复测。

## 硬件

- MacBook M5 Max (Mac)
- 参考价格: 未公开，见来源

## 模型

- Qwen3.6-27B-MTPLX-Optimized-Speed · `MLXCommunity 4-bit 主干 + 3-bit draft LM head（MTP depth 3）`
- 下载: [huggingface.co/Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed](https://huggingface.co/Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed)

## 引擎

- MTPLX
- 备注: MTPLX v0.1.0-preview

## 启动命令

```bash
brew install youssofal/mtplx/mtplx && mtplx start
```

## 关键参数

- 上下文: —
- 并发: 单请求
- 标签: `3bit`, `4bit`, `dense`, `speculative`, `MTP`

## 预期速度

- 63.056 tok/s 生成 (📣 宣称)

## 注意事项

- 非一手实测（宣称/转述），实际速度可能不同。
- HF 模型卡（作者自报）; 关思考模式，draft 温度 0.70，fanmax；内存未写
- 速度随驱动、引擎版本、上下文长度和提示长度变化。

## 来源与致谢

- [https://huggingface.co/Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed](https://huggingface.co/Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed)
- 版权归原作者；本页仅摘要并链接。数据以 CC BY 4.0 发布。
