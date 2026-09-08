"""autodl_minimax（MiniMax v2 原生）适配器测试。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from ai import VideoPrompt, VideoStatus
from ai.providers.autodl_minimax import AutoDLMiniMaxVideo
from ai.providers.autodl_minimax import gateway


def _make() -> AutoDLMiniMaxVideo:
    return AutoDLMiniMaxVideo()


def test_model_default() -> None:
    assert _make().model_name == "MiniMax-H3"


def test_build_request_content_array() -> None:
    g = _make()
    p = VideoPrompt(
        scene="s", subject="t", duration_hint=8,
        reference_image_url=["https://a/1.png", "https://a/2.png"],
        reference_video_url=["https://v/ref.mp4"],
        reference_audio_url=["https://au/ref.mp3"],
        style="cinematic portrait 9:16, 2K", resolution="2K",
    )
    body = g.build_request(p)
    assert body["model"] == "MiniMax-H3"
    assert body["duration"] == 8 and body["resolution"] == "2K" and body["ratio"] == "9:16"
    kinds = [c["type"] for c in body["content"]]
    assert kinds.count("image_url") == 2
    assert kinds.count("video_url") == 1
    assert kinds.count("audio_url") == 1
    assert body["content"][1]["role"] == "reference_image"


def test_duration_clamped_4_15() -> None:
    g = _make()
    assert g.build_request(VideoPrompt(scene="x", subject="y", duration_hint=20))["duration"] == 15
    assert g.build_request(VideoPrompt(scene="x", subject="y", duration_hint=1))["duration"] == 4


def test_resolution_mapping() -> None:
    g = _make()
    assert g.build_request(VideoPrompt(scene="x", subject="y", resolution="1080p竖"))["resolution"] == "2K"
    assert g.build_request(VideoPrompt(scene="x", subject="y", resolution="480p竖"))["resolution"] == "768P"
    with pytest.raises(ValueError, match="resolution"):
        g.build_request(VideoPrompt(scene="x", subject="y", resolution="4K竖"))


def test_estimate_cost_member() -> None:
    g = _make()
    assert abs(g.estimate_cost(5, "2K") - 4.00) < 1e-9
    assert abs(g.estimate_cost(5, "2K", member=True) - 3.60) < 1e-9


def test_parse_response_both_shapes() -> None:
    r1 = gateway.parse_response(
        {"task_id": "t1", "status": "Success", "data": {"file_url": "https://o/v.mp4"}}, "t1"
    )
    assert r1.status == VideoStatus.COMPLETED and r1.video_url == "https://o/v.mp4"
    # comfyui 风格（含 type 字段）也能被 MiniMax 网关容忍
    r2 = gateway.parse_response(
        {"code": "Success", "data": {"status": "completed", "results": [{"url": "u", "type": "video"}]}}, "t2"
    )
    assert r2.status == VideoStatus.COMPLETED and r2.video_url == "u"
    r3 = gateway.parse_response({"code": "Error", "msg": "bad"}, "t3")
    assert r3.status == VideoStatus.FAILED
