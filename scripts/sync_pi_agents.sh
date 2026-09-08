#!/usr/bin/env bash
# 同步 .claude/agents → .pi/agents，做 pi 工具名映射。
#
# 背景：.claude/agents/*.md 的 frontmatter 用 Claude 大写工具名（Read/Write/Edit/Bash/WebFetch），
# pi 的 --tools 是大小写敏感的严格 allowlist，子 agent 拿到全大写的 allowlist 会静默丢失全部文件工具。
# pi-subagents 的 agentOverrides 只补 frontmatter 未设的字段（frontmatter 优先），无法覆盖，
# 因此 .pi/agents 必须是实体目录 + 小写工具名，由本脚本生成。
#
# 用法：bash scripts/sync_pi_agents.sh
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=.pi/agents
rm -rf "$OUT"
mkdir -p "$OUT"

for f in .claude/agents/*.md; do
  name=$(basename "$f")
  if grep -q "^tools:.*WebFetch" "$f"; then
    # 研究型 agent：Claude WebFetch/WebSearch → pi web 工具（pi-web-access 扩展提供）
    sed -E 's|^tools:.*|tools: read, write, edit, bash, web_search, fetch_content, get_search_content, source_check|' \
      "$f" >"$OUT/$name"
  else
    sed -E 's|^tools: Read, Write, Edit, Bash$|tools: read, write, edit, bash|' \
      "$f" >"$OUT/$name"
  fi
done

echo "synced $(ls "$OUT" | wc -l | tr -d ' ') agents → $OUT/"
grep -H "^tools:" "$OUT"/*.md || true
