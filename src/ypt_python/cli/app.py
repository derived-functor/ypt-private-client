from __future__ import annotations

import typer

from ypt_python.commands import auth, groups, logs, ranks, study

app = typer.Typer(
    help="Unofficial YPT study-time tracker client.",
    no_args_is_help=True,
)

app.add_typer(auth.app, name=None)
app.add_typer(study.app, name="study")
app.add_typer(groups.app, name="groups")
app.add_typer(ranks.app, name="rank")
app.add_typer(logs.app, name="logs")


def main() -> None:
    app()


if __name__ == "__main__":
    main()