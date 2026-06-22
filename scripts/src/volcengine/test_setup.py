"""
Volcengine SDK 自检脚本。
运行：  uv run --directory scripts python -m volcengine.test_setup
"""

import sys


def main():
    print("=" * 50)
    print("Volcengine SDK Setup Test")
    print("=" * 50)

    # 1. 凭证检查
    print("\n[1/4] Credentials...")
    try:
        from volcengine._auth import get_credentials
        creds = get_credentials()
        print(f"  AK: {creds.ak[:12]}...")
        print(f"  SK: {creds.sk[:12]}...")
        print(f"  API Key: {'✓' if creds.api_key else '✗'}")
    except Exception as e:
        print(f"  FAIL: {e}")
        return 1

    # 2. 模型定义
    print("\n[2/4] Data models...")
    try:
        from volcengine.models import VideoPrompt, TTSOptions, MusicPrompt

        vp = VideoPrompt(
            scene="medium shot",
            subject="test subject",
            camera="static camera",
            duration_hint=5,
        )
        assert "medium shot" in vp.to_natural_language()

        tts = TTSOptions(text="测试文本", speed=1.0)
        assert tts.text == "测试文本"

        mp = MusicPrompt(genres=["Electronic"], bpm=95, duration_hint=50)
        assert mp.bpm == 95

        print("  VideoPrompt ✓")
        print("  TTSOptions  ✓")
        print("  MusicPrompt ✓")
    except Exception as e:
        print(f"  FAIL: {e}")
        return 1

    # 3. 注册表
    print("\n[3/4] Registry...")
    try:
        from volcengine.registry import (
            available_models,
            check_connectivity,
            get_config,
        )

        models = available_models()
        print(f"  Video providers: {models['video']}")
        print(f"  TTS providers:   {models['tts']}")
        print(f"  Music providers: {models['music']}")

        connectivity = check_connectivity()
        assert connectivity.get("credentials_ok"), "Credentials not found"
        print("  Connectivity check: ✓")
    except Exception as e:
        print(f"  FAIL: {e}")
        return 1

    # 4. 服务实例化（不调用 API）
    print("\n[4/4] Service instantiation...")
    try:
        from volcengine.seedance import SeedanceVideo
        from volcengine.tts import VolcengineTTS
        from volcengine.genbgm import VolcengineBGM

        video = SeedanceVideo()
        assert video._model

        tts = VolcengineTTS()
        assert tts._api_key

        bgm = VolcengineBGM()
        assert bgm._host

        print("  SeedanceVideo ✓")
        print("  VolcengineTTS  ✓")
        print("  VolcengineBGM  ✓")
    except Exception as e:
        print(f"  FAIL: {e}")
        return 1

    print("\n" + "=" * 50)
    print("All checks passed. SDK is ready for agent use.")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
