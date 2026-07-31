"""
Stock finder CLI — search and download stock footage/images.

Usage (standalone):
    uv run --directory scripts stock search video "funny cat" --count 5
    uv run --directory scripts stock search image "sunset" --source pixabay
    uv run --directory scripts stock download <url> -o output.mp4

Usage (ai subcommand):
    uv run --directory scripts ai stock search video "funny cat"
"""

import sys
import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

# Ensure scripts/src/ is on sys.path so stock_finder resolves.
_scripts_src = Path(__file__).resolve().parent.parent
if str(_scripts_src) not in sys.path:
    sys.path.insert(0, str(_scripts_src))

from stock_finder import (
    search_videos,
    search_images,
    download_video,
    download_image,
    StockFinderError,
    AuthError,
    RateLimitError,
)

console = Console()


# ── Error handler ──────────────────────────────────────────


def _handle_error(e):
    """Print a user-friendly error and exit."""
    if isinstance(e, AuthError):
        console.print(f"[red]API Key error:[/] {e}")
        console.print("  Set PEXELS_API_KEY or PIXABAY_API_KEY in your environment.")
    elif isinstance(e, RateLimitError):
        console.print(f"[yellow]Rate limited:[/] {e}")
        console.print("  Wait a moment or use a different source.")
    elif isinstance(e, StockFinderError):
        console.print(f"[red]Error:[/] {e}")
    else:
        console.print(f"[red]Unexpected error:[/] {e}")
    sys.exit(1)


# ── CLI group ──────────────────────────────────────────────


@click.group(name="stock")
def cli():
    """Search and download stock footage & images.

    Sources: Pexels (default), Pixabay.

    Set PEXELS_API_KEY or PIXABAY_API_KEY in your environment.
    """


@cli.group()
def search():
    """Search stock media by keyword."""


@search.command("video")
@click.argument("query")
@click.option("--count", "-n", default=10, type=int, help="Number of results (max 80)")
@click.option(
    "--source",
    default="pexels",
    type=click.Choice(["pexels", "pixabay"]),
    help="Stock provider",
)
@click.option("--json", "json_output", is_flag=True, help="Output raw JSON")
def search_video_cmd(query, count, source, json_output):
    """Search stock video footage by QUERY."""
    try:
        results = search_videos(query, count=count, source=source)
    except (AuthError, RateLimitError, StockFinderError) as e:
        _handle_error(e)

    if json_output:
        console.print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if not results:
        console.print("[yellow]No videos found.[/]")
        return

    table = Table(title=f"Stock Videos — {source} ({len(results)} results)")
    table.add_column("#", style="dim")
    table.add_column("ID", style="cyan")
    table.add_column("Dur", style="green")
    table.add_column("Resolution", style="blue")
    table.add_column("Description", style="white", no_wrap=False)
    table.add_column("URL (truncated)", style="magenta", max_width=32)

    for i, r in enumerate(results, 1):
        desc = r["description"]
        if len(desc) > 48:
            desc = desc[:45] + "..."
        url_short = r["url"]
        if len(url_short) > 30:
            url_short = url_short[:27] + "..."
        table.add_row(
            str(i),
            r["id"],
            f"{r['duration']}s" if r["duration"] else "?",
            f"{r['width']}x{r['height']}" if r["width"] else "?",
            desc,
            url_short,
        )
    console.print(table)


@search.command("image")
@click.argument("query")
@click.option("--count", "-n", default=10, type=int, help="Number of results (max 80)")
@click.option(
    "--source",
    default="pexels",
    type=click.Choice(["pexels", "pixabay"]),
    help="Stock provider",
)
@click.option("--json", "json_output", is_flag=True, help="Output raw JSON")
def search_image_cmd(query, count, source, json_output):
    """Search stock images by QUERY."""
    try:
        results = search_images(query, count=count, source=source)
    except (AuthError, RateLimitError, StockFinderError) as e:
        _handle_error(e)

    if json_output:
        console.print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if not results:
        console.print("[yellow]No images found.[/]")
        return

    table = Table(title=f"Stock Images — {source} ({len(results)} results)")
    table.add_column("#", style="dim")
    table.add_column("ID", style="cyan")
    table.add_column("Resolution", style="blue")
    table.add_column("URL (truncated)", style="magenta", max_width=40)

    for i, r in enumerate(results, 1):
        url_short = r["url"]
        if len(url_short) > 37:
            url_short = url_short[:34] + "..."
        table.add_row(
            str(i),
            r["id"],
            f"{r['width']}x{r['height']}" if r["width"] else "?",
            url_short,
        )
    console.print(table)


@cli.command()
@click.argument("url")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output file path")
def download(url, output):
    """Download a stock media file from URL.

    Works for both videos and images. The URL comes from search results.
    """
    out_path = Path(output)
    try:
        console.print(f"[bold]Downloading...[/]")
        console.print(f"  From: {url}")
        console.print(f"  To:   {out_path}")
        result = download_video(url, out_path)
        size_mb = result.stat().st_size / (1024 * 1024)
        console.print(f"[green]Downloaded:[/] {result} ({size_mb:.1f} MB)")
    except (AuthError, RateLimitError, StockFinderError) as e:
        _handle_error(e)


# Export for integration as `ai stock` subcommand.
# This is the same Click group object, reusable as a subcommand.
stock_group = cli

if __name__ == "__main__":
    cli()
