import typer
from sqlify import Sqlite3Sqlify, build_typer_cli, Migrations

from common import provider

migrations_service = Migrations(
    migrations_path="migrations/",
    sqlify=provider.get_instance(Sqlite3Sqlify),
)

app = typer.Typer()
app.add_typer(build_typer_cli(migrations_service=migrations_service), name="db")

if __name__ == "__main__":
    app()
