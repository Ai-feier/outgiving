# 踩坑与解决

> 来源：HANDOFF.md（已归位）、content-pipeline skill 故障排查、reflecting-log。按场景组织，症状 → 原因 → 解决。

## 内容管线

| 症状 | 原因 | 解决 |
|------|------|------|
| `validate` 报「未知 kind」 | frontmatter 缺字段 | 用 `content new` / `content adapt` 重新生成 |
| `transition` 报「不允许 X→Y」 | 跳过状态链 | 走完整链，如 draft→reviewing→ready |
| 命令找不到 | 未安装依赖 | `cd scripts && uv sync` |
| preview 端口占用 | 残留进程 | `pkill -f "content preview"` 后重启 |
| preview 图片 404 | 用了 `../../../` 相对路径 | 改用 `assets/figN.svg` |
| 中文路径 404 | preview 编码问题 | 重启服务；检查 `unquote` 是否重复调用 |

## 素材与资产

| 症状 | 原因 | 解决 |
|------|------|------|
| 重复生产资产 | 跳过 asset-lab 直接生产 | 先查子索引再产——重复生产是素材系统熵增第一来源 |
| 版本号比较错误 | `v9` vs `v10` 按字典序 | 语义版本比较（`v10` > `v9`） |
| 跨风格复用冲突 | 未终裁 | script-designer 只标记「候选复用」，visual-designer 六维终裁 |
| 归档误伤 | archived 前未查 `appears_in` | 有 active 选题仍在引用则不能归档 |
| 修订 vs 变体混淆 | 小修改与上下文变更未区分 | 小修改→Revision（版本号递增）；新妆造/季节→Variant（新建条目 + `derived_from`） |

## 视频管线

| 症状 | 原因 | 解决 |
|------|------|------|
| 参考图过密降质量 | >7 张 | 生视频 3-7 张（KeyFrame-Compass：密度↑忠实度↓） |
| 段间漂移 | 未用尾帧 | 非首段必用前段末帧（尾帧链） |
| 版权拦截 | 特征组合触发（Seedance） | 按角色域拆分生成段，特征级规避 |
| 参考图未声明 | prompt / 确认门缺清单 | 每次生图/生视频必须声明参考图清单 + 负面参考 |

## 生成与工具

| 症状 | 原因 | 解决 |
|------|------|------|
| AI 生成失败 / 空结果 | API key 未配置 | `.env` 中配置 `ARK_API_KEY` |
| figure-draftsman 辅助工具缺失 | drawmode / excalidraw-mcp-server 未安装 | 使用前按 figure-draftsman.md「辅助工具」安装 |
| Seedance 参考图版本不一致 | 全生态版本号未同步 | 一致性审计轮跨读对齐（reflecting 3.1.6） |
