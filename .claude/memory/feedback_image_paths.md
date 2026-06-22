---
name: 内容图片路径用 assets/ 不用相对路径
description: 在 content-pipeline 的正文 md 中嵌入图片时，统一用 ![](assets/figN.svg)，不要用 ../../../topics/...
type: feedback
originSessionId: 41ed1b79-b6e6-4704-8c8b-1cc70d9bcaf7
---
正文 md 里嵌入图片，统一用 `![](assets/figN.svg)`，**不要**用 `../../../topics/T0XX-.../assets/figN.svg`。

**Why:** 2026-06-22 踩坑——article.md 写了 4 个 `..`，从 `platforms/wechat/T0XX-.../` 到 repo root 只需 3 个，第 4 个 `..` 跑出 repo root 被 preview 安全检查拦截，图片 404。相对路径层级太脆弱，文件挪位置就断。

**How to apply:** figure-draftsman agent 嵌图时一律用 `![](assets/figN.svg)`，preview 服务器（`scripts/src/content/preview.py` 的 `_rewrite_src`）会自动把 `assets/` 解析为 md 所在 topic 的 assets 目录。brief.md 已经是这样，正文也要对齐。
