# AGENTS.md — scripts/src AI 生成基础设施

本目录是内容管线的**执行引擎**：AI 生成（图/视频/音频）、内容数据模型、视频编辑。
本文档是代码架构指南——读完它，你应该能独立找到改动点并正确修改。

> 分层已落地（2026-08）：`volcengine/` → `ai/`（核心层）+ `ai/providers/`（实现层）。
> 旧 `volcengine` 包仅剩兼容 shim（Deprecated，转发到 ai.*）。

## 导航

| 层 | 入口 | 性质 |
| ---- | ------ | ------ |
| 核心层 | `ai/` | provider 无关：模型/注册表/CLI/凭证分发 |
| 实现层 | `ai/providers/` | 一个 provider 一个子包 |
| 其他子系统 | `content/` `editor/` `stock_finder/` `web_fetcher/` | 与 ai/ 无依赖，各司其职 |

## 架构总览

Provider-agnostic：**`ai` CLI → 注册表 → 适配器**。默认火山引擎（Seedance 视频 / Seedream 图像），
可经 `model_config.json` 或环境变量切换 provider（含 autodl 网关）。

```text
scripts/src/
├── ai/                          # 核心层：provider 无关
│   ├── __init__.py              # 公共导出
│   ├── interfaces.py            # Protocol 服务契约（互换前提）
│   ├── models.py                # 语义模型
│   ├── registry.py              # 服务工厂 + available_models/check_connectivity
│   ├── cli.py                   # `ai` CLI（纯语义装配，provider 无关）
│   ├── cli_verify.py            # verify / extract-lastframe 命令
│   ├── cli_edit.py              # edit 命令组（compose/clip/concat/speed/mute/profile）
│   ├── formats.py               # 标准 video-prompt.md 9 要素解析（通用兜底格式）
│   ├── json_types.py            # 响应信封 TypedDict（ComfyUI/MiniMax/ARK）
│   ├── auth.py                  # 凭证分发（聚合各 provider 的 check()）
│   ├── _utils.py                # image_to_data_uri 等
│   ├── model_config.json        # provider 选择（env 可覆盖）
│   └── providers/               # 实现层
│       ├── volcengine/          # 火山引擎（Seedance/Seedream/TTS/BGM）
│       ├── autodl_comfyui/      # AutoDL ComfyUI workflow API（H3 多图参考）
│       └── autodl_minimax/      # AutoDL MiniMax v2 原生 API
├── content/                     # 内容管线：topic/draft/published 数据模型
├── editor/                      # 视频编辑：compose/clip/concat/speed/mute/profile
├── stock_finder/                # 素材搜索
└── web_fetcher/                 # curl_cffi 下载（绕过 Cloudflare）
```

**唯一依赖方向规则**：核心层 → providers（工厂在运行时懒加载）；适配器只依赖 `ai.models`

+ 自家 `auth.py`。**禁止 providers 之间横向依赖**。违反此规则 = 架构退化，review 打回。

## 目录地图

| 文件 | 职责 |
| --- | --- |
| `ai/models.py` | 语义模型：`VideoPrompt`/`ImagePrompt`/`TTSOptions`/`MusicPrompt` + 对应 Result。**不绑定任何 API 格式** |
| `ai/interfaces.py` | Protocol：`VideoGenerator`/`ImageGenerator`/`TTSProvider`/`MusicProvider`。适配器实现即互换 |
| `ai/registry.py` | `get_video_generator(model)` / `get_image_generator` / `get_tts` / `get_music_generator`；`get_config` / `available_models` / `check_connectivity` |
| `ai/cli.py` | `ai` 命令树（generate/extract-lastframe/verify/edit）。provider 无关的分支逻辑在这层 |
| `ai/auth.py` | `provider_credentials_ok(name)` / `all_credentials()`——只聚合，不硬编码某家 .env 格式 |
| `ai/_utils.py` | `image_to_data_uri`（本地图 → base64）、`validate_reference_image` |
| `ai/model_config.json` | 当前 provider 选择（env `*_PROVIDER` 覆盖） |
| `ai/providers/volcengine/` | `seedance.py`（视频）/`seedream.py`（图像）/`tts.py`/`genbgm.py` + `auth.py`（VOLC_AK/SK、ARK_API_KEY）+ `http.py`（Signature V4 签名） |
| `ai/providers/autodl_comfyui/` | **迁移中**。ComfyUI workflow 客户端（H3 多图参考生视频） |
| `ai/providers/autodl_minimax/` | **迁移中**。MiniMax 原生 v2 视频生成客户端 |

## 语义层与适配器的关系

`models.py` 的 Prompt 是**人对视频/图像的描述语义**（scene/subject/camera/…），不是任何厂商的请求体。
每个 adapter 负责翻译：语义模型 → 自家 API 请求格式。因此——

**更换模型提供商 = 写一个新 adapter（实现 Protocol），注册表 + 配置一行切换，语义模型不动。**
新增语义字段（如 `VideoPrompt.resolution`/`raw_prompt`）放 `models.py`；已有适配器不用的字段直接忽略。

## 注册表与配置

provider 选择顺序：`model_config.json` → 环境变量覆盖（`VIDEO_PROVIDER` / `IMAGE_PROVIDER` / `TTS_PROVIDER` / `MUSIC_PROVIDER`）。

| 服务 | 注册表入口 | provider 值 |
| --- | --- | --- |
| 视频 | `get_video_generator()` | `seedance`（默认）/ `autodl_comfyui` / `autodl_minimax` |
| 图像 | `get_image_generator()` | `seedream`（默认） |
| TTS | `get_tts()` | `volcengine` |
| 音乐 | `get_music_generator()` | `volcengine_genbgm` |

凭证（`.env`，不硬编码）：

| 变量 | 用途 |
| --- | --- |
| `VOLC_AK` / `VOLC_SK` | 火山 OpenAPI 签名 |
| `ARK_API_KEY` | Seedance/Seedream ARK API |
| `AUTODL_API_KEY` | autodl.art 令牌（令牌管理 → ComfyUI 组），comfyui 与 minimax 两个接入点共用 |

## 新增 provider 步骤清单

1. 建 `ai/providers/<name>/`：`auth.py`（读自家凭证，暴露 `check() -> bool` 不抛异常）+ 适配器
2. 适配器实现对应 Protocol（如 `VideoGenerator`：`submit`/`query`/`wait`/`submit_with_retry`，返回语义 Result）
3. `ai/registry.py` 加分支 + 更新 `available_models()`
4. `ai/model_config.json` note 补充可用 provider；切换走 env
5. 额外能力（如 `build_request` 供 dry-run、成本估算）用 `hasattr` 探测，不进基础契约
6. 更新本 AGENTS.md 目录地图

## CLI 速查

```bash
# 图像
uv run --directory scripts ai generate image --prompt "..." -o out.png   # 可 -r 参考图 / --prompt-file

# 视频（provider-agnostic）
uv run --directory scripts ai generate video --scene "..." --subject "..." -o ./out/
# --prompt-file 读 video-prompt.md（标准 9 要素）或 video-prompt-h3.md（H3 三核心字段）
#   格式解析归 provider（parse_prompt_file），CLI 不认识任何 provider
# --resolution（provider 专属枚举，透传） / --dry-run（预览请求体不花钱） / --seed / --ref-images（本地或 URL）

# 后处理与自评估
uv run --directory scripts ai extract-lastframe in.mp4 -o frame.png
uv run --directory scripts ai verify in.mp4 --expect-duration 15 --expect-resolution 1080x1920
# 编辑：ai edit compose --manifest / clip / concat / speed / mute / profile
```

## autodl 两个接入点（新增能力）

同一家网关（autodl.art）、两套 API 家族，共用 `AUTODL_API_KEY`。

### autodl_comfyui — ComfyUI workflow API

+ 提交：`POST /api/v1/comfyui/comfyui_workflow/{workflow_id}`；查询：`GET .../result/{task_id}`（轮询，404 → 未就绪）
+ H3 多图参考 workflow：`minimax_h3_lightx2v_v5`
+ 输入：`prompt`（必填）/ `duration`（1-10s 整数，默认 5）/ `resolution`（9 档预设：480p竖/横、768p竖/横、1080p竖/横、480p/768p/1080p(1:1)）/ `seed`（选填）/ `ref_image_0..8`（URL，JPG/PNG/WebP）
+ **约束：`ref_image_0` 必填**——多图参考至少要 1 张参考图；纯文生视频走 seedance 等 T2VA
+ 价格：480p/768p ¥0.01/秒，1080p ¥0.10/秒

### autodl_minimax — MiniMax 原生 v2 API

+ 提交：`POST /api/v1/minimax/v2/video_generation`（原生 MiniMax v2，模型 `MiniMax-H3`，多模态 content 数组：文本/图片/视频/音频）
+ 价格：768P ¥0.45-0.50/秒，2K ¥0.72-0.80/秒（会员 9 折）
+ 输入素材：音频免费；图片 5 张内免费、超出 ¥0.18-0.20/张；视频按输入时长计费（与生成分辨率同价）
+ schema 已核实（aiping 网关 + MiniMax 官方 v2 文档一致）；**任务查询端点路径待实测**（env `AUTODL_MINIMAX_QUERY_PATH` 可覆盖）
+ 约束：时长 4-15s；分辨率 768P/2K；reference_* 与首尾帧互斥

## 约定

+ **同步 API**：agent 直接 `submit()` → `wait()`；轮询与重试封装在适配器内
+ **结构化输入输出**：Pydantic/dataclass 模型，不传裸 dict
+ **凭证不硬编码**：一律 `.env` + 各 provider `auth.py`
+ **HTTP**：标准库 `urllib`，不引入 requests 等新依赖
+ **错误**：provider 自己的错误类型（如 `VolcError` 风格），包装 HTTP 状态码 + 可读 message
+ **JSON 类型纪律**：响应解析用 `ai/json_types.py` 的 TypedDict 信封，边界 cast 一次，内部零 cast
+ **测试**：`uv run --directory scripts --group dev pytest tests/` 全绿后再合入
+ **Python 3.11+ / Click / rich**；改动后 `uv sync` + `ai --help` 自检

## 凭证

+ `AUTODL_API_KEY`（autodl.art 令牌，ComfyUI 组）——需在项目根 `.env` 填入真实令牌
