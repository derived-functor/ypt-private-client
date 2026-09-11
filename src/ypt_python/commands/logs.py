from __future__ import annotations

from datetime import date

import typer
from rich.panel import Panel

from ypt_python.cli.output import console, format_ms, make_subject_table
from ypt_python.cli.runtime import YPTClient, authenticated

app = typer.Typer(help="Study logs.", no_args_is_help=True)


@app.command()
def day(
    date_str: str = typer.Argument(None, help="Date in YYYY-MM-DD. Defaults to today."),
) -> None:
    """Show your study log for a day."""
    if date_str is None:
        date_str = date.today().strftime("%Y-%m-%d")

    async def _impl(client: YPTClient) -> None:
        with console.status(f"Loading log for {date_str}..."):
            log = await client.logs.day(date_str)
        console.print(Panel(f"[bold]{log.date or date_str}[/]", title="Study log", border_style="cyan", padding=(1, 2)))
        if log.subjects:
            console.print(make_subject_table([(s.subject_title, s.study_ms) for s in log.subjects]))
        body = f"[green]{format_ms(log.study_ms)}[/] study    [blue]{format_ms(log.rest_ms)}[/] rest"
        console.print(Panel(body, title="Total", border_style="cyan", padding=(0, 2)))

    authenticated(_impl)()