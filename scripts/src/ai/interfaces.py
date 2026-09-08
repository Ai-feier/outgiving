"""
Provider 服务接口（Protocol）。核心层只依赖这里的契约，不依赖具体实现。

设计原则：
- 注册表（registry）在运行时懒加载具体适配器，满足 Protocol 即可互换
- 更换模型提供商 = 写新的 adapter（实现同签名），注册表 + 配置一行切换
- 可选能力（parse_prompt_file / build_request / estimate_cost）用 hasattr 探测，
  不进基础契约——缺失时调用方走通用兜底，不影响互换性
"""

from __future__ import annotations

from typing import Any, Protocol

from ai.models import (
    ImagePrompt,
    ImageResult,
    MusicPrompt,
    MusicResult,
    TTSOptions,
    TTSResult,
    VideoPrompt,
    VideoResult,
)


class VideoGenerator(Protocol):
    """视频生成器契约。所有 video provider 必须实现。"""

    def submit(self, prompt: VideoPrompt) -> VideoResult:
        """提交生成任务，返回 task_id，不阻塞。"""
        ...

    def query(self, task_id: str) -> VideoResult:
        """查询任务状态。"""
        ...

    def wait(
        self, task_id: str, poll_interval: int = 10, timeout: int = 600
    ) -> VideoResult:
        """轮询直到完成或超时。"""
        ...

    def submit_with_retry(self, prompt: VideoPrompt, max_retries: int = 3) -> VideoResult:
        """提交并等待，失败自动重试。"""
        ...

    # ── 可选能力（调用方 hasattr 探测）──────────────────────

    def parse_prompt_file(self, content: str) -> VideoPrompt | None:
        """解析本 provider 的专属 prompt 文件格式；不识别时返回 None。"""
        ...

    def build_request(self, prompt: VideoPrompt) -> dict[str, Any]:
        """预览 API 请求体（CLI --dry-run）。"""
        ...

    def estimate_cost(self, duration: int, resolution: str) -> float:
        """估算生成成本（元）。"""
        ...


class ImageGenerator(Protocol):
    """图像生成器契约。"""

    def generate(self, prompt: ImagePrompt) -> ImageResult:
        """同步生成，直接返回结果。"""
        ...

    def generate_to_file(self, prompt: ImagePrompt, output_path: str) -> ImageResult:
        """生成并下载到文件。"""
        ...


class TTSProvider(Protocol):
    """语音合成契约。"""

    def synthesize(self, options: TTSOptions) -> TTSResult:
        """文本 → 音频。"""
        ...


class MusicProvider(Protocol):
    """音乐生成契约。"""

    def generate(self, prompt: MusicPrompt) -> MusicResult:
        """生成音乐，返回任务 id 与音频 URL。"""
        ...
