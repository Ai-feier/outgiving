# AI 基础设施

> 权威源：`CLAUDE.md`「基础设施」+ `scripts/src/`——本文为人读架构摘要。

## 结构

```
scripts/
├── pyproject.toml        # Python 3.11+, Click + rich
├── src/
│   ├── content/          # 内容管线 CLI（frontmatter schema 校验）
│   ├── volcengine/       # AI 生成（provider-agnostic 注册表 + 适配器）
│   │   ├── registry.py     # 注册表：get_image_generator / get_video_generator
│   │   ├── model_config.json  # provider 切换（或环境变量 VIDEO_PROVIDER）
│   │   ├── seedance.py      # Seedance 2.0 视频适配器（submit→query→wait 异步轮询）
│   │   ├── seedream.py      # Seedream 5.0 图像适配器
│   │   └── cli.py           # ai 命令入口（--provider 切换）
│   ├── web_fetcher/      # 参考素材下载（curl_cffi 浏览器指纹，绕过 Cloudflare）
│   ├── editor/           # 编辑器工具
│   └── stock_finder/     # 素材查找
├── ai-video/             # 视频项目工作区（projects/TXXX/ + gates/ + assets/）
└── assets/               # 视觉资产库（asset-lab 管理）
```

## AI 生成架构

```
ai CLI → 注册表（get_image_generator / get_video_generator）→ 适配器
```

- **provider-agnostic**：agent 不依赖具体实现，通过注册表获取服务；切换 provider 只改配置，不改调用方
- 默认：Seedance 2.0（视频）/ Seedream 5.0（图像）；可切换 Kling / Veo / H3（MiniMax）
- 视频生成入口：`ai generate video` 支持 `--scene/--subject` 直接参数，或 `--prompt-file`（读取 video-prompt.md / video-prompt-h3.md 格式）
- 自评估门：`ai verify`（ffprobe 元数据 + 首2s/中点/末2s 关键帧抽样 + PASS/FAIL 退出码）——与 provider 无关
- H3 适配器：**未实施**（待 API 实测与门 0 裁决，见 `docs/pipeline/video-pipeline.md` H3 节）

## 配置与密钥

- provider 切换：`scripts/src/volcengine/model_config.json` 或环境变量 `VIDEO_PROVIDER` / `IMAGE_PROVIDER`
- 视频 API 密钥：`.env` 中 `ARK_API_KEY`（火山引擎）
- 首次使用：`cd scripts && uv sync`；git hook：`git config core.hooksPath .githooks`

## 命令入口

完整命令速查见 `docs/operations/cli.md`。内容管线（content 系列）与 AI 生成（ai 系列）两组命令，均通过 `uv run --directory scripts` 调用。
