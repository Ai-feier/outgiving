"""autodl_comfyui（H3 多图参考）适配器测试。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai import VideoPrompt, VideoStatus
from ai.providers.autodl_comfyui import AutoDLComfyUIVideo
from ai.providers.autodl_comfyui import gateway, h3_prompt


def _make() -> AutoDLComfyUIVideo:
    return AutoDLComfyUIVideo()


def test_workflow_default() -> None:
    assert _make().workflow == "minimax_h3_lightx2v_v5"


def test_build_request_full() -> None:
    g = _make()
    p = VideoPrompt(
        scene="medium shot", subject="dev typing", duration_hint=8, seed=42,
        reference_image_url=["https://a/1.png", "https://a/2.png"],
        resolution="1080p竖",
    )
    body = g.build_request(p)
    assert body["duration"] == 8
    assert body["resolution"] == "1080p竖"
    assert body["seed"] == 42
    assert body["ref_image_0"] == "https://a/1.png"
    assert body["ref_image_1"] == "https://a/2.png"
    assert "ref_image_2" not in body


def test_duration_clamped_to_10() -> None:
    g = _make()
    p = VideoPrompt(scene="x", subject="y", duration_hint=15, reference_image_url=["https://a/1.png"])
    assert g.build_request(p)["duration"] == 10


def test_no_ref_raises() -> None:
    g = _make()
    with __import__("pytest").raises(ValueError, match="reference image"):
        g.build_request(VideoPrompt(scene="x", subject="y"))


def test_invalid_resolution_raises() -> None:
    g = _make()
    with __import__("pytest").raises(ValueError, match="resolution"):
        g.build_request(VideoPrompt(scene="x", subject="y", reference_image_url=["https://a/1.png"], resolution="8K竖"))


def test_estimate_cost() -> None:
    g = _make()
    assert abs(g.estimate_cost(5, "1080p竖") - 0.50) < 1e-9
    assert abs(g.estimate_cost(5, "768p竖") - 0.05) < 1e-9


def test_parse_response_status_spellings() -> None:
    r1 = gateway.parse_response(
        {"code": "Success", "data": {"status": "completed", "results": [{"url": "v.mp4", "type": "video"}]}}, "t1"
    )
    assert r1.status == VideoStatus.COMPLETED and r1.video_url == "v.mp4"
    r2 = gateway.parse_response(
        {"code": "Success", "data": {"status": "SUCCESS", "results": [{"url": "u", "type": "video"}]}}, "t2"
    )
    assert r2.status == VideoStatus.COMPLETED
    r3 = gateway.parse_response({"code": "Error", "msg": "bad"}, "t3")
    assert r3.status == VideoStatus.FAILED and r3.error_message == "bad"


def test_parse_prompt_file_h3() -> None:
    content = """# T

**输入模式**: I2VA

For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic, a woman walks.

overall_soundscape: rain pattering.

non_diegetic_music: soft piano.
"""
    p = h3_prompt.parse_prompt_file(content)
    assert p is not None
    assert p.raw_prompt.startswith("For the target video, at 0.00 seconds")
    assert "integrated_multimodal_description: [Shot 1] Cinematic" in p.raw_prompt
    assert "overall_soundscape: rain pattering." in p.raw_prompt


def test_parse_prompt_file_standard_returns_none() -> None:
    assert h3_prompt.parse_prompt_file("- **scene**: medium shot") is None
