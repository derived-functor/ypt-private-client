from __future__ import annotations

import time
from pathlib import Path

import typer
from rich.panel import Panel

from ypt_python._models import DayLog
from ypt_python.cli.output import console, format_ms, make_subject_table
from ypt_python.cli.runtime import YPTClient, authenticated

app = typer.Typer(help="Study timer control.", no_args_is_help=True)

_STATE_FILE = Path("~/.cache/ypt-python/study_started_at").expanduser()
_DEFAULT_DEVICE = "ypt-cli"


@app.command()
def start(
    subject: str = typer.Argument(..., help="Subject title to start studying."),
    device_model: str = typer.Option(_DEFAULT_DEVICE, "--device-model", help="Device model reported to the API."),
) -> None:
    """Start studying a subject and record the session start time."""

    async def _impl(client: YPTClient) -> None:
        with console.status("Starting study session..."):
            day = await client.study.start(subject, device_model)
        _save_started_at(_now_ms())
        body = f"Subject: [bold]{subject}[/]"
        console.print(Panel(body, title="Study started", border_style="green", padding=(1, 2)))
        _print_day_summary(day)

    authenticated(_impl)()


@app.command()
def stop(
    started_at: int = typer.Option(None, "--started-at", help="Session start epoch ms. Defaults to the recorded one."),
    device_model: str = typer.Option(_DEFAULT_DEVICE, "--device-model", help="Device model reported to the API."),
) -> None:
    """Stop the study timer."""

    if started_at is None:
        started_at = _load_started_at()
        if started_at is None:
            console.print(
                "[red]No recorded session start.[/] "
                "Pass it with [bold]--started-at[/] (epoch ms).",
            )
            raise typer.Exit(1)

    async def _impl(client: YPTClient) -> None:
        with console.status("Stopping study session..."):
            day = await client.study.stop(started_at, device_model)
        _clear_started_at()
        console.print(Panel("Session stopped.", title="Study stopped", border_style="red", padding=(1, 2)))
        _print_day_summary(day)

    authenticated(_impl)()


def _print_day_summary(day: DayLog) -> None:
    if day.subjects:
        console.print(make_subject_table([(s.subject_title, s.study_ms) for s in day.subjects]))
    body = f"[green]{format_ms(day.study_ms)}[/] study    [blue]{format_ms(day.rest_ms)}[/] rest"
    console.print(Panel(body, title="Day total", border_style="cyan", padding=(0, 2)))


def _now_ms() -> int:
    return int(time.time() * 1000)


def _save_started_at(ts: int) -> None:
    _STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    _STATE_FILE.write_text(str(ts), encoding="utf-8")


def _load_started_at() -> int | None:
    try:
        raw = _STATE_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def _clear_started_at() -> None:
    try:
        _STATE_FILE.unlink()
    except OSError:
        pass