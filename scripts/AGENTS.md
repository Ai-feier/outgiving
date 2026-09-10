# AGENTS.md — scripts 执行引擎

本目录是内容生产的**执行引擎**：生成（图/视频/音频）、编辑、校验、内容数据模型。
命令在仓库任意位置运行：`uv run --directory scripts <命令>`。代码架构与 `ai` 命令树细节见 [`src/AGENTS.md`](src/AGENTS.md)。

## 内容管线

| 命令 | 用途 |
| --- | --- |
| `content list` | 选题总览（**任何动作前先 list**） |
| `content new "<标题>"` | 新建选题，分配 T0XX |
| `content adapt T001 wechat` | 派生渠道草稿（自动递增 revision） |
| `content show T001` | 选题详情（所有衍生物） |
| `content transition <doc_id> <status>` | 推进状态（schema 校验合法转移，不手改 status） |
| `content validate` | 全量 frontmatter 校验 |
| `content index` | 重建 `.content-index.json` |
| `content stats` | 全局统计 |
| `content preview [T001]` | 浏览器并排预览（0.0.0.0:8765） |

## AI 生成（provider-agnostic，默认火山引擎）

见 [`src/AGENTS.md`](src/AGENTS.md)「CLI 速查」——`ai generate image` / `ai generate video`（`--prompt-file`）/ `ai extract-lastframe` / `ai verify` / `ai edit`。切换 provider 走 `ai/model_config.json` 或环境变量。

## 工具

| 命令 | 用途 |
| --- | --- |
| `web-fetcher download <url> -o <path>` | 参考素材下载（curl_cffi 浏览器指纹，绕过 Cloudflare） |

## 环境

- **渠道名仅 4 个**：`wechat` / `xiaohongshu` / `x` / `douyin`
- 首次：`cd scripts && uv sync`；git hook：`git config core.hooksPath .githooks`
- 视频 API 密钥：仓库根 `.env` 中 `ARK_API_KEY`
