"""
web_fetcher CLI — 浏览器指纹伪装的 HTTP 下载。

用法:
    # 下载图片
    uv run --directory scripts python -m web_fetcher download https://example.com/img.jpg -o ref.jpg

    # 快捷命令（需要先 uv sync）
    uv run --directory scripts web-fetcher download https://example.com/img.jpg -o ref.jpg

    # 抓取 HTML 页面
    uv run --directory scripts python -m web_fetcher fetch https://example.com

    # 使用 Safari 指纹 + 指定超时
    uv run --directory scripts python -m web_fetcher download <url> -o out.jpg -f safari17_0 -t 60

    # 列出可用指纹
    uv run --directory scripts python -m web_fetcher list-fingerprints
"""

from __future__ import annotations

import json
import sys

import click

from web_fetcher import (
    FINGERPRINTS,
    WebFetchError,
    WebFetcher,
    UnsupportedContentType,
)


# ── 全局选项 ────────────────────────────────────────────────────


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--verbose", "-v", is_flag=True, help="输出详细日志")
def cli(verbose: bool) -> None:
    if verbose:
        import logging

        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


# ── download 子命令 ─────────────────────────────────────────────


@cli.command()
@click.argument("url")
@click.option("--output", "-o", required=True, help="输出文件路径")
@click.option(
    "--fingerprint",
    "-f",
    default="chrome131",
    show_default=True,
    help=f"浏览器指纹（可用: {', '.join(sorted(FINGERPRINTS))}）",
)
@click.option("--timeout", "-t", default=30.0, type=float, show_default=True, help="请求超时秒数")
@click.option("--retry", "-r", default=3, type=int, show_default=True, help="最大重试次数")
def download(
    url: str,
    output: str,
    fingerprint: str,
    timeout: float,
    retry: int,
) -> None:
    """下载图片到本地文件。验证 Content-Type 是否为图片。"""
    try:
        fetcher = WebFetcher(
            fingerprint=fingerprint,
            timeout=timeout,
            max_retries=retry,
        )
        path = fetcher.download_image(url, output)
        click.echo(f"OK {path}")
    except UnsupportedContentType as e:
        click.echo(f"ERROR Content-Type 不是图片: {e.content_type}", err=True)
        sys.exit(2)
    except WebFetchError as e:
        click.echo(f"ERROR {e}", err=True)
        sys.exit(1)
    except ValueError as e:  # 无效的 fingerprint
        click.echo(f"ERROR {e}", err=True)
        sys.exit(1)


# ── fetch 子命令 ────────────────────────────────────────────────


@cli.command()
@click.argument("url")
@click.option(
    "--fingerprint",
    "-f",
    default="chrome131",
    show_default=True,
    help="浏览器指纹",
)
@click.option("--timeout", "-t", default=30.0, type=float, show_default=True, help="请求超时秒数")
@click.option("--retry", "-r", default=3, type=int, show_default=True, help="最大重试次数")
@click.option("--json-output", "-j", is_flag=True, help="以 JSON 格式输出（检测到 JSON 响应时自动）")
def fetch(url: str, fingerprint: str, timeout: float, retry: int, json_output: bool) -> None:
    """抓取 URL 内容（HTML 或 JSON）。输出到 stdout。"""
    try:
        fetcher = WebFetcher(
            fingerprint=fingerprint,
            timeout=timeout,
            max_retries=retry,
        )
        text = fetcher.fetch_page(url)

        if json_output:
            data = json.loads(text)
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            click.echo(text, nl=False)

    except WebFetchError as e:
        click.echo(f"ERROR {e}", err=True)
        sys.exit(1)
    except ValueError as e:  # 无效的 fingerprint 或 JSON 解析失败
        if json_output:
            click.echo(f"WARN 内容不是有效 JSON: {e}", err=True)
            sys.exit(2)
        click.echo(f"ERROR {e}", err=True)
        sys.exit(1)


# ── check 子命令 ────────────────────────────────────────────────


@cli.command()
@click.argument("url")
@click.option(
    "--fingerprint",
    "-f",
    default="chrome131",
    show_default=True,
    help="浏览器指纹",
)
@click.option("--timeout", "-t", default=15.0, type=float, show_default=True, help="请求超时秒数")
def check(url: str, fingerprint: str, timeout: float) -> None:
    """检查 URL 可访问性（HEAD 请求）。返回状态码和响应头。"""
    try:
        fetcher = WebFetcher(fingerprint=fingerprint, timeout=timeout, max_retries=1)
        headers = fetcher.head(url)
        click.echo(f"OK {url}")
        for k, v in sorted(headers.items()):
            click.echo(f"  {k}: {v}")
    except WebFetchError as e:
        click.echo(f"ERROR {e}", err=True)
        sys.exit(1)


# ── list-fingerprints 子命令 ────────────────────────────────────


@cli.command(name="list-fingerprints")
def list_fingerprints() -> None:
    """列出所有可用的浏览器指纹。"""
    click.echo("可用浏览器指纹:")
    for name, bt in sorted(FINGERPRINTS.items()):
        click.echo(f"  {name}")


if __name__ == "__main__":
    cli()
