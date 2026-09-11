from __future__ import annotations

import typer
from rich.panel import Panel
from rich.table import Table

from ypt_python._models import Group, GroupMember
from ypt_python.cli.output import console, duration_color, format_ms
from ypt_python.cli.runtime import YPTClient, authenticated

app = typer.Typer(help="Study groups.", no_args_is_help=True)


@app.command()
def browse(
    category_id: int = typer.Option(0, "--category-id", help="Category id to filter by."),
    page: int = typer.Option(1, "--page", help="Page number."),
    country_id: int = typer.Option(None, "--country-id", help="Country id."),
) -> None:
    """Browse public study groups."""

    async def _impl(client: YPTClient) -> None:
        with console.status("Browsing groups..."):
            groups = await client.groups.browse(category_id=category_id, page=page, country_id=country_id)
        if not groups:
            console.print("No groups found.", style="yellow")
            return
        console.print(_groups_table(groups))

    authenticated(_impl)()


@app.command()
def my() -> None:
    """List groups you have joined."""

    async def _impl(client: YPTClient) -> None:
        with console.status("Loading your groups..."):
            groups = await client.groups.my_groups()
        if not groups:
            console.print("You have not joined any groups.", style="yellow")
            return
        console.print(_groups_table(groups))

    authenticated(_impl)()


@app.command()
def members(
    group_id: int = typer.Argument(..., help="Group id."),
    country_id: int = typer.Option(0, "--country-id", help="Country id."),
) -> None:
    """List members of a group."""

    async def _impl(client: YPTClient) -> None:
        with console.status("Loading members..."):
            members = await client.groups.members(group_id, country_id)
        if not members:
            console.print("No members found.", style="yellow")
            return
        table = Table(title=f"Group {group_id} members", header_style="bold cyan")
        table.add_column("Nickname", style="white")
        table.add_column("Study time", justify="right")
        table.add_column("Status")
        for m in members:
            status = "[green]studying[/]" if m.studying else "[grey50]idle[/]"
            table.add_row(m.nickname, f"[{duration_color(m.study_ms)}]{format_ms(m.study_ms)}[/]", status)
        console.print(table)

    authenticated(_impl)()


def _groups_table(groups: list[Group]) -> Table:
    table = Table(title="Groups", header_style="bold cyan")
    table.add_column("ID", justify="right")
    table.add_column("Title", style="white")
    table.add_column("Owner")
    table.add_column("Members", justify="right")
    for g in groups:
        table.add_row(str(g.id), g.title, g.owner, str(g.member_count))
    return table