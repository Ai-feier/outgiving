"""workbench — 视频提示词工作台（web 端看/改/提意见）。

- markdown 文件是唯一事实源（agent 与 CLI 照旧读写）
- web 是视图层：块级查看、块级编辑（写回 md）、批注（annotations.md）
- 请求体层：复用 ai.providers 的 parse/build_request，"看到的就是要发出去的"
"""
