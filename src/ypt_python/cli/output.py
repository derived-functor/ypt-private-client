"""Helpers for pretty Rich output."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def format_ms(ms: int) -> str:
    """Format milliseconds as a compact human-readable duration."""
    total = max(0, int(ms)) // 1000
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m"
    if m:
        return f"{m}m {s:02d}s"
    return f"{s}s"


def duration_color(ms: int) -> str:
    """Pick a color based on study amount."""
    h = ms / 3_600_000
    if h >= 3:
        return "bold green"
    if h >= 1:
        return "green"
    if h > 0:
        return "yellow"
    return "grey50"


def make_subject_table(rows: list[tuple[str, int]]) -> Table:
    table = Table(title="Subjects", show_header=True, header_style="bold cyan")
    table.add_column("Subject", style="white")
    table.add_column("Study time", justify="right")
    for title, ms in rows:
        table.add_row(title, f"[{duration_color(ms)}]{format_ms(ms)}[/]")
    return table


def panel(title: str, body: str, border_style: str = "cyan") -> Panel:
    return Panel(body, title=title, border_style=border_style, padding=(1, 2))