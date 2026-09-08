"""registry 切换与 CLI 装配测试。"""

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from click.testing import CliRunner

from ai import get_video_generator
from ai import registry
from ai.cli import cli
from ai.formats import parse_standard_prompt_file
from ai.providers.autodl_comfyui import AutoDLComfyUIVideo
from ai.providers.autodl_minimax import AutoDLMiniMaxVideo


def test_registry_env_switch(video_provider: Callable[[str], None]) -> None:
    video_provider("autodl_comfyui")
    assert isinstance(get_video_generator(), AutoDLComfyUIVideo)
    video_provider("autodl_minimax")
    assert isinstance(get_video_generator(), AutoDLMiniMaxVideo)
    video_provider("seedance")
    assert type(get_video_generator()).__name__ == "SeedanceVideo"


def test_standard_format_parse() -> None:
    p = parse_standard_prompt_file("- **scene**: medium shot\n- **subject**: a woman\n- **style**: cinematic, portrait")
    assert p.scene == "medium shot"
    assert p.subject == "a woman"
    assert "portrait" in p.style
    # CLI 显式传参优先
    p2 = parse_standard_prompt_file("- **scene**: from file", scene="from cli")
    assert p2.scene == "from cli"


def test_cli_dry_run_h3(tmp_path: Path, video_provider: Callable[[str], None]) -> None:
    video_provider("autodl_comfyui")
    pf = tmp_path / "video-prompt-h3.md"
    pf.write_text(
        "integrated_multimodal_description: [Shot 1] a woman walks.\n\n"
        "overall_soundscape: rain.\n\n"
        "non_diegetic_music: piano.\n"
    )
    img = tmp_path / "ref.png"
    img.write_bytes(b"fake")
    runner = CliRunner()
    r = runner.invoke(cli, ["generate", "video", "--prompt-file", str(pf), "--dry-run", "--ref-images", str(img)])
    assert r.exit_code == 0, r.output
    assert "ref_image_0" in r.output
    assert "integrated_multimodal_description" in r.output


def test_cli_dry_run_h3_no_refs(tmp_path: Path, video_provider: Callable[[str], None]) -> None:
    video_provider("autodl_comfyui")
    pf = tmp_path / "video-prompt-h3.md"
    pf.write_text("integrated_multimodal_description: [Shot 1] a woman walks.\n")
    runner = CliRunner()
    r = runner.invoke(cli, ["generate", "video", "--prompt-file", str(pf), "--dry-run"])
    assert r.exit_code == 0, r.output
    assert "requires at least 1 reference image" in r.output


def test_cli_dry_run_standard(tmp_path: Path, video_provider: Callable[[str], None]) -> None:
    video_provider("seedance")
    pf = tmp_path / "video-prompt.md"
    pf.write_text("- **scene**: medium shot, rainy street\n- **subject**: a woman with umbrella\n")
    runner = CliRunner()
    r = runner.invoke(cli, ["generate", "video", "--prompt-file", str(pf), "--dry-run"])
    assert r.exit_code == 0, r.output
    assert "rainy street" in r.output


def test_cli_command_tree() -> None:
    runner = CliRunner()
    r = runner.invoke(cli, ["--help"])
    for cmd in ("generate", "edit", "verify", "extract-lastframe", "stock"):
        assert cmd in r.output, cmd
