"""仓库级检查门 —— 唯一入口，一条命令跑完全部结构约定。

跑法::

    uv run --directory scripts check_harness.py

失败即非零退出，逐条输出 ``[PASS]/[FAIL]`` 与命中的 ``文件:行 —— 原因``。

判定口径与 [`system/CONVENTIONS.md`](../system/CONVENTIONS.md)「检查门」一一对应：

1. 顶层只有允许项
2. 每个 skill 有消费者
3. 渠道名不出现在路径中
4. 共有维度只在唯一权威文件出现
5. 相对引用可解析
6. 每个 skill 含例子段
7. 「平台」零残留

本文件是全部判定的作者源；口径变更先改这里，再把同一条口径写回 CONVENTIONS.md。
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 归档与运行期产物不参与判定：归档是冻结历史，产物由 .gitignore 排除。
ARCHIVE_PREFIX = "products/_archive/"
SKIP_DIRS = {".git", "__pycache__", ".venv", ".pytest_cache", ".ruff_cache", "node_modules"}

# ---------------------------------------------------------------- 检查 1
# 依据：用户裁决 + CONVENTIONS.md「目录约定」——顶层恰好 7 项 + 两份入口文件；
# git 机制文件由检查门放行（当前只有 .gitignore，.githooks/ 已计入 7 项）。
ALLOWED_TOP_DIRS = {".agents", ".githooks", ".pi", "assets", "products", "scripts", "system"}
ALLOWED_ROOT_FILES = {"AGENTS.md", "CONTEXT.md"}
GIT_MECHANISM_FILES = {".gitignore"}

# ---------------------------------------------------------------- 检查 2
# 消费面：岗位、硬约束、其他 skill、产品设计、根入口。
CONSUMER_GLOBS = (
    ".pi/agents/*.md",
    ".pi/rules/*.md",
    ".pi/skills/**/*.md",
    "system/*.md",
    "AGENTS.md",
)

# 显式豁免（键 = skill 名或 skill 组目录名）。豁免必须写明理由，且只豁免「消费关系」这一项。
SKILL_EXEMPT = {
    "ask": "入口 skill：由 system/PRODUCT.md「入口」节按名字消费，全仓无路径引用",
    "engineering": "通用工具包（外部引入），非本仓流水线",
    "productivity": "通用工具包（外部引入），非本仓流水线",
    "reflecting": "全体岗位消费的机制：按路径引用计数即通过（writer.md、video-director.md）",
}

# ---------------------------------------------------------------- 检查 3
CHANNEL_NAMES = ("wechat", "xiaohongshu", "x", "douyin")
# `.pi/skills/channels/<channel>.md` 是 CONVENTIONS 定义的渠道卡文件名，天然含渠道名，不属扫描面。
CHANNEL_PATH_SCOPE = ("products/", "assets/", "scripts/")

# ---------------------------------------------------------------- 检查 4
CHANNELS_MD = ".pi/skills/channels/CHANNELS.md"
RHYTHM_MD = ".pi/skills/rhythm/SKILL.md"
VISUAL_WORLD_MD = ".pi/skills/visual-world/SKILL.md"

# 共有维度的数值词表：每个数值在 `.pi/skills/**` 内只能命中唯一权威文件（可多次命中同一文件）。
#
# 精确匹配口径：短数值（组块上限、通道堆叠上限、钩子「前 3 秒」）单独看会与正文里的巧合数字和
# 其他维度的数值撞车（如 `≤3` 同时是「组块上限」与「实体复现拍数上限」的量级），因此这几条以
# 「表格单元」形态入表——它正是渠道表里那格的字面值，既不放大也不漏判。
SHARED_VALUES: tuple[tuple[str, str, str], ...] = (
    # (数值, 维度, 唯一权威文件)
    ("2000–4000 字", "字数/时长", CHANNELS_MD),
    ("200–500 字", "字数/时长", CHANNELS_MD),
    ("800–1500 字", "字数/时长", CHANNELS_MD),
    ("≤280 字符", "字数/时长", CHANNELS_MD),
    ("≤4000 字", "字数/时长", CHANNELS_MD),
    ("60–90s", "字数/时长", CHANNELS_MD),
    ("30–60s", "字数/时长", CHANNELS_MD),
    ("| ≤15 |", "感知组块上限", CHANNELS_MD),
    ("| 3–6 |", "感知组块上限", CHANNELS_MD),
    ("| ≤5 |", "感知组块上限", CHANNELS_MD),
    ("| ≤3 |", "感知组块上限", CHANNELS_MD),
    ("前 3 句", "钩子位置", CHANNELS_MD),
    ("≤30 字", "钩子位置", CHANNELS_MD),
    ("前 10 字", "钩子位置", CHANNELS_MD),
    ("前 50 字", "钩子位置", CHANNELS_MD),
    ("前 60 字符", "钩子位置", CHANNELS_MD),
    ("前 3 秒", "钩子位置", CHANNELS_MD),
    ("≤6s", "单拍时长上限", RHYTHM_MD),
    ("≤8s", "单拍时长上限", RHYTHM_MD),
    ("1.5–2.0", "认知负荷 CL", RHYTHM_MD),
    ("| ≤2 |", "通道堆叠上限", RHYTHM_MD),
    ("≤3 拍", "实体复现拍数上限", VISUAL_WORLD_MD),
    ("≤5 拍", "实体复现拍数上限", VISUAL_WORLD_MD),
)

# ---------------------------------------------------------------- 检查 6
# 例子段的可判定最小结构：ATX 标题含「例子 / 真例 / 示例 / 实例 / Example」，
# 或一个围栏代码块同时含「输入」与「输出」（英文 Input/Output 同理）。
EXAMPLE_HEADING_RE = re.compile(r"例子|真例|示例|实例|example", re.IGNORECASE)

# 「有真例」是本仓的质量标准，只对本仓作者源的 skill 生效——不对别人的源文件施加。
# 与检查 2 的豁免同源：通用工具包与外部锁定 skill 不属本仓流水线。
EXAMPLE_EXEMPT = {
    "engineering": "通用工具包（外部引入），非本仓作者源",
    "productivity": "通用工具包（外部引入），非本仓作者源",
    "h3-prompt-writing": "外部锁定 skill（`.pi/skills-lock.json` 锁定 MiniMax 官方源），不重写其内容",
}

# ---------------------------------------------------------------- 检查 7
# 行级白名单：只豁免「必须点出被禁词」的规则行本身。整行文本入表——行内容一旦改动，白名单即失效。
PLATFORM_TERM = "平台"
PLATFORM_WHITELIST: tuple[tuple[str, str], ...] = (
    ("system/CONVENTIONS.md", "- 不在路径、字段、文档里使用「平台」指代渠道"),
    (
        "system/CONVENTIONS.md",
        (
            "7. 「平台」零残留——扫路径与文件内容；豁免「必须点出被禁词」的规则行本身，以及不指代内容出口的云服务商名称"
            "（行级白名单，条目与理由见 `scripts/check_harness.py`）"
        ),
    ),
    # 云服务商名称，不指代内容出口；生成通路代码不改。
    ("scripts/src/ai/providers/volcengine/seedream.py", "Volcengine ARK 平台，支持文生图/图生图/组图生成。"),
    ("scripts/src/ai/providers/volcengine/seedance.py", "Volcengine ARK 平台，支持文生视频/图生视频/视频编辑/延长。"),
)
# `.pi/rules/channels.md` 的规则行（「不用任何旧称」）当前不含被禁词，故无需白名单条目。
# 检查器与其自测必须写出被禁词才能定义并验证本检查，不参与本检查。
PLATFORM_SCAN_SKIP = {"scripts/check_harness.py", "scripts/tests/test_check_harness.py"}

FENCE_RE = re.compile(r"^\s*```")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SKILL_PATH_RE = re.compile(r"\.pi/skills/[^\s`)\]\"'<>]+?/SKILL\.md")
INLINE_PATH_RE = re.compile(r"`([^`\n]+)`")
INLINE_PATH_ROOT = (".pi/", "system/", "scripts/")
INLINE_PATH_SUFFIX = re.compile(r"\.(md|py|json|txt|sh|ya?ml|toml|svg|png|mp4)$")
PLACEHOLDER_RE = re.compile(r"[<>{}*]")


@dataclass(frozen=True)
class Finding:
    """一条失败命中。``check`` 是检查项标题，``message`` 带定位与原因。"""

    check: str
    message: str


# ---------------------------------------------------------------- 基础设施


def repo_files(root: Path) -> list[str]:
    """仓库内的文件清单（相对 POSIX 路径）。

    优先取 git 视角（tracked + untracked 但未被 ignore），把 `.gitignore` 排掉的构建产物与
    运行期状态挡在判定之外；不在 git 仓库里（测试夹具）时退化为文件系统遍历。
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            capture_output=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return sorted(
            p.relative_to(root).as_posix()
            for p in root.rglob("*")
            if p.is_file() and not _skipped(p.relative_to(root))
        )
    return sorted(
        rel
        for rel in (Path(chunk.decode()).as_posix() for chunk in out.split(b"\0") if chunk)
        if (root / rel).is_file()  # 已删但未提交的路径不在树上，不参与判定
    )


def _skipped(rel: Path) -> bool:
    return any(part in SKIP_DIRS for part in rel.parts)


def _read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="replace")


def skill_files(root: Path) -> list[str]:
    """`.pi/skills/**/SKILL.md`，相对仓库根。"""
    return [p for p in repo_files(root) if p.startswith(".pi/skills/") and p.endswith("/SKILL.md")]


def skill_key(rel: str) -> str:
    """`.pi/skills/engineering/tdd/SKILL.md` → `engineering/tdd`。"""
    return rel[len(".pi/skills/") : -len("/SKILL.md")]


def is_exempt(rel: str) -> bool:
    key = skill_key(rel)
    return key in SKILL_EXEMPT or key.split("/")[0] in SKILL_EXEMPT


def resolve_ref(root: Path, from_file: Path, target: str) -> Path | None:
    """把引用解析成绝对路径。仓库根优先，其次引用者所在目录。"""
    if PLACEHOLDER_RE.search(target):
        return None
    for base in (root, from_file.parent):
        candidate = (base / target).resolve()
        if candidate.exists():
            return candidate
    return None


def prose_lines(path: Path) -> Iterator[tuple[int, str]]:
    """逐行产出正文，跳过围栏代码块与 HTML 注释（模板/示例里的路径不是仓库引用）。"""
    in_fence = False
    in_comment = False
    for number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = raw
        if in_fence:
            if FENCE_RE.match(line):
                in_fence = False
            continue
        if FENCE_RE.match(line):
            in_fence = True
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            head, _, tail = line.partition("<!--")
            if "-->" not in tail:
                in_comment = True
            line = head
        yield number, line


def fenced_blocks(text: str) -> Iterator[str]:
    block: list[str] = []
    inside = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            if inside:
                yield "\n".join(block)
                block = []
            inside = not inside
            continue
        if inside:
            block.append(line)
    if block:
        yield "\n".join(block)


# ---------------------------------------------------------------- 检查 1


def check_top_level(root: Path) -> list[str]:
    dirs: set[str] = set()
    files: set[str] = set()
    for rel in repo_files(root):
        head, sep, _ = rel.partition("/")
        if sep:
            dirs.add(head)
        else:
            files.add(head)
    findings: list[str] = []
    for name in sorted(dirs - ALLOWED_TOP_DIRS):
        findings.append(
            f"{name}/ —— 未允许的顶层项（允许 {' '.join(sorted(ALLOWED_TOP_DIRS))}）"
        )
    for name in sorted(files - ALLOWED_ROOT_FILES - GIT_MECHANISM_FILES):
        findings.append(
            f"{name} —— 未允许的根文件（允许 AGENTS.md / CONTEXT.md / {' '.join(sorted(GIT_MECHANISM_FILES))}）"
        )
    return findings


# ---------------------------------------------------------------- 检查 2


def _consumer_refs(root: Path, rel: str) -> set[str]:
    """一个消费文件里出现过的仓库路径（markdown 链接解析结果 + 字面 skill 路径）。"""
    text = _read(root, rel)
    refs = set(SKILL_PATH_RE.findall(text))
    for target in MD_LINK_RE.findall(text):
        target = target.split('"')[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = resolve_ref(root, root / rel, target.split("#")[0])
        if resolved is not None:
            refs.add(resolved.relative_to(root.resolve()).as_posix())
    return refs


def check_skill_consumers(root: Path) -> list[str]:
    consumers = [
        rel
        for rel in repo_files(root)
        if rel.endswith(".md")
        and not rel.startswith(ARCHIVE_PREFIX)
        and not rel.startswith("products/")
        and (rel in ("AGENTS.md",) or rel.startswith((".pi/agents/", ".pi/rules/", ".pi/skills/", "system/")))
    ]
    refs = {rel: _consumer_refs(root, rel) for rel in consumers}
    findings: list[str] = []
    for skill in skill_files(root):
        if is_exempt(skill):
            continue
        used_by = [rel for rel in consumers if rel != skill and skill in refs[rel]]
        if not used_by:
            findings.append(f"{skill} —— 无消费者：没有任何别的文件引用它的路径")
    return findings


# ---------------------------------------------------------------- 检查 3


def _is_channel_name(segment: str) -> bool:
    """路径段是不是渠道名。`wechat` 与 `T001-wechat`（选题 id + 渠道 slug）都算。"""
    return any(segment == name or segment.endswith(f"-{name}") for name in CHANNEL_NAMES)


def check_channel_in_paths(root: Path) -> list[str]:
    findings: list[str] = []
    for rel in repo_files(root):
        if rel.startswith(ARCHIVE_PREFIX):
            continue
        parts = rel.split("/")
        if len(parts) > 1 and not rel.startswith(CHANNEL_PATH_SCOPE):
            continue
        for segment in parts[:-1]:
            if _is_channel_name(segment):
                findings.append(f"{rel} —— 路径段 `{segment}` 是渠道名")
        stem = parts[-1].rsplit(".", 1)[0]
        if _is_channel_name(stem):
            findings.append(f"{rel} —— 文件名 `{stem}` 是渠道名")
    return findings


# ---------------------------------------------------------------- 检查 4


def check_shared_values(root: Path) -> list[str]:
    files = [rel for rel in repo_files(root) if rel.startswith(".pi/skills/") and rel.endswith((".md", ".txt"))]
    texts = {rel: _read(root, rel) for rel in files}
    findings: list[str] = []
    for value, dimension, canonical in SHARED_VALUES:
        hits = sorted(rel for rel, text in texts.items() if value in text)
        if hits == [canonical]:
            continue
        others = [rel for rel in hits if rel != canonical]
        if not hits:
            findings.append(f"{canonical} —— 「{dimension}」的数值 `{value}` 不在唯一权威文件里")
        elif others:
            findings.append(
                f"{'、'.join(others)} —— 「{dimension}」的数值 `{value}` 在 `{canonical}` 之外重复定义"
            )
    return findings


# ---------------------------------------------------------------- 检查 5


def check_relative_refs(root: Path) -> list[str]:
    findings: list[str] = []
    for rel in repo_files(root):
        if not rel.endswith(".md") or rel.startswith(ARCHIVE_PREFIX):
            continue
        path = root / rel
        for number, line in prose_lines(path):
            for target in MD_LINK_RE.findall(line):
                target = target.split('"')[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if PLACEHOLDER_RE.search(target):
                    continue
                if resolve_ref(root, path, target.split("#")[0]) is None:
                    findings.append(f"{rel}:{number} —— 链接目标不存在：{target}")
            if not rel.startswith(INLINE_PATH_ROOT):
                continue
            for token in INLINE_PATH_RE.findall(line):
                token = token.strip()
                if not token or " " in token or "://" in token:
                    continue
                if not token.startswith(INLINE_PATH_ROOT) or not INLINE_PATH_SUFFIX.search(token):
                    continue
                if PLACEHOLDER_RE.search(token):
                    continue
                if resolve_ref(root, path, token) is None:
                    findings.append(f"{rel}:{number} —— 反引号内路径不存在：{token}")
    return findings


# ---------------------------------------------------------------- 检查 6


def check_skill_examples(root: Path) -> list[str]:
    findings: list[str] = []
    for rel in skill_files(root):
        if skill_key(rel) in EXAMPLE_EXEMPT or skill_key(rel).split("/")[0] in EXAMPLE_EXEMPT:
            continue
        text = _read(root, rel)
        if any(
            EXAMPLE_HEADING_RE.search(line)
            for line in text.splitlines()
            if line.startswith("#")
        ):
            continue
        if any(
            ("输入" in block and "输出" in block)
            or ("input" in block.lower() and "output" in block.lower())
            for block in fenced_blocks(text)
        ):
            continue
        findings.append(f"{rel} —— 无例子段：既无「例子/真例/示例/Example」标题，也无输入→输出代码块")
    return findings


# ---------------------------------------------------------------- 检查 7


def check_platform_term(root: Path) -> list[str]:
    allowed = {(rel, line) for rel, line in PLATFORM_WHITELIST}
    findings: list[str] = []
    for rel in repo_files(root):
        if rel.startswith(ARCHIVE_PREFIX) or rel in PLATFORM_SCAN_SKIP:
            continue
        path = root / rel
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(lines, 1):
            if PLATFORM_TERM not in line or (rel, line) in allowed:
                continue
            findings.append(f"{rel}:{number} —— 「{PLATFORM_TERM}」残留：{line.strip()[:60]}")
    return findings


# ---------------------------------------------------------------- 入口

CHECKS: tuple[tuple[str, Callable[[Path], list[str]]], ...] = (
    ("1 顶层只有允许项", check_top_level),
    ("2 每个 skill 有消费者", check_skill_consumers),
    ("3 渠道名不出现在路径中", check_channel_in_paths),
    ("4 共有维度只在唯一权威文件出现", check_shared_values),
    ("5 相对引用可解析", check_relative_refs),
    ("6 每个 skill 含例子段", check_skill_examples),
    ("7 「平台」零残留", check_platform_term),
)


def run(root: Path = ROOT) -> list[Finding]:
    """跑完全部检查，返回全部命中（空列表 = 全绿）。"""
    return [Finding(title, message) for title, check in CHECKS for message in check(root)]


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = ROOT
    if args[:1] == ["--root"]:
        root = Path(args[1]).resolve()
    findings = run(root)
    grouped: dict[str, list[str]] = {}
    for finding in findings:
        grouped.setdefault(finding.check, []).append(finding.message)

    for title, _ in CHECKS:
        messages = grouped.get(title, [])
        print(f"[{'FAIL' if messages else 'PASS'}] {title}")
        for message in messages:
            print(f"       - {message}")

    print("\n行级白名单（豁免见 check_harness.py 注释）：")
    for rel, line in PLATFORM_WHITELIST:
        print(f"       - 检查 7 | {rel}: {line}")

    total = len(findings)
    print(f"\n{'FAIL' if total else 'PASS'} —— 共 {total} 条命中")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
