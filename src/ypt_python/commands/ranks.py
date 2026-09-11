from __future__ import annotations

from datetime import date

import typer
from rich.table import Table

from ypt_python.cli.output import console, duration_color, format_ms
from ypt_python.cli.runtime import YPTClient, authenticated

app = typer.Typer(help="Ranks and leaderboards.", no_args_is_help=True)


@app.command()
def me(
    category_id: int = typer.Option(0, "--category-id", help="Category id."),
    country_id: int = typer.Option(0, "--country-id", help="Country id."),
) -> None:
    """Show your rank in a category."""

    async def _impl(client: YPTClient) -> None:
        with console.status("Fetching your rank..."):
            rank = await client.ranks.my_rank(category_id, country_id)
        if rank is None:
            console.print("No rank available.", style="yellow")
            return
        console.print(f"Your rank: [bold cyan]#{rank}[/]")

    authenticated(_impl)()


@app.command()
def top(
    category_id: int = typer.Option(0, "--category-id", help="Category id."),
    country_id: int = typer.Option(0, "--country-id", help="Country id."),
    page: int = typer.Option(1, "--page", help="Page number."),
    date_str: str = typer.Option(None, "--date", help="Date in YYYY-MM-DD. Defaults to today."),
    limit: int = typer.Option(20, "--limit", help="Max rows to show."),
) -> None:
    """Show the category leaderboard."""
    if date_str is None:
        date_str = date.today().strftime("%Y-%m-%d")

    async def _impl(client: YPTClient) -> None:
        with console.status("Fetching leaderboard..."):
            result = await client.ranks.category_members(category_id, country_id, date_str, page=page)
        if not result.members:
            console.print("No leaderboard data.", style="yellow")
            return
        table = Table(title=f"Leaderboard {date_str}", header_style="bold cyan")
        table.add_column("#", justify="right")
        table.add_column("Nickname", style="white")
        table.add_column("Study time", justify="right")
        for i, m in enumerate(result.members[:limit], start=(page - 1) * 20 + 1):
            table.add_row(str(i), m.nickname, f"[{duration_color(m.study_ms)}]{format_ms(m.study_ms)}[/]")
        console.print(table)

    authenticated(_impl)()