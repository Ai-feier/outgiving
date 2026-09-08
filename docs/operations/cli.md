# CLI 操作手册

> 权威源：`.claude/rules/project/workflow.md`（内容管线）+ `CLAUDE.md`「命令」。所有命令在仓库任意位置运行：`uv run --directory scripts <命令>`。

## 内容管线

| 命令 | 用途 |
|------|------|
| `content list` | 选题总览（**任何动作前先 list**） |
| `content new "<标题>"` | 新建选题，分配 T0XX，生成 brief + outline |
| `content adapt T001 wechat` | 派生平台草稿（自动递增 revision） |
| `content show T001` | 选题详情（所有衍生物） |
| `content transition <doc_id> <status>` | 推进状态（schema 校验合法转移，不手改 status） |
| `content validate` | 全量 frontmatter 校验 |
| `content index` | 重建 `.content-index.json` |
| `content stats` | 全局统计 |
| `content preview [T001]` | 浏览器四平台并排预览（0.0.0.0:8765） |

## AI 生成（provider-agnostic，默认火山引擎）

| 命令 | 用途 |
|------|------|
| `ai generate image --prompt "..." -o out.png` | 图像生成（Seedream 5.0 默认） |
| `ai generate video --scene "..." --subject "..." -o ./out/` | 视频生成（Seedance 默认；`--prompt-file` 读取 video-prompt.md / video-prompt-h3.md） |
| `ai extract-lastframe in.mp4 -o frame.png` | 提取末帧（段间锚定用） |
| `ai verify in.mp4 --expect-duration 15 --expect-resolution 1080x1920` | 生成后自评估门（ffprobe + 关键帧抽样，PASS/FAIL 退出码） |

## 工具

| 命令 | 用途 |
|------|------|
| `web-fetcher download <url> -o <path>` | 参考素材下载（curl_cffi 浏览器指纹，绕过 Cloudflare） |

## 环境

- **平台名仅 4 个**：`wechat` / `xiaohongshu` / `x` / `douyin`
- 首次：`cd scripts && uv sync`；`git config core.hooksPath .githooks`
- 视频 API 密钥：`.env` 中 `ARK_API_KEY`

## 故障排查

见 `docs/troubleshooting/index.md`（validate 报错 / preview 404 / 端口占用等）。
