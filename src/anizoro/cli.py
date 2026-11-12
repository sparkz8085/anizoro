"""Anizoro command-line interface."""
import typer
from rich.console import Console
from rich.table import Table
from anizoro import __version__
from anizoro.database import Database
from anizoro.player import PlayerError, play
from anizoro.providers.base import ProviderError
from anizoro.providers.registry import get_provider, list_providers

app = typer.Typer(name="anizoro", help="Terminal-first anime discovery and playback launcher.",
                  no_args_is_help=True)
console = Console()

@app.command()
def version():
    """Show installed version."""
    console.print(f"Anizoro {__version__}")

@app.command()
def providers():
    """List provider adapters."""
    table = Table("Provider", "Description")
    for provider in list_providers():
        table.add_row(provider.name, provider.description)
    console.print(table)

@app.command()
def search(query: str = typer.Argument(...),
           provider: str = typer.Option("anilist", "--provider", "-p")):
    """Search an anime catalogue."""
    try:
        results = get_provider(provider).search(query)
    except (ProviderError, ValueError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1) from exc
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return
    table = Table("No.", "Title", "ID", "Provider")
    for i, anime in enumerate(results, 1):
        table.add_row(str(i), anime.title, anime.id, anime.provider)
    console.print(table)

@app.command()
def add(anime_id: str, title: str, url: str = typer.Option("", "--url")):
    """Add an anime to the local watchlist."""
    Database().add(anime_id, title, url or None)
    console.print(f"[green]Saved:[/green] {title}")

@app.command()
def watchlist():
    """Show saved anime."""
    rows = Database().list_watchlist()
    if not rows:
        console.print("[yellow]Your watchlist is empty.[/yellow]")
        return
    table = Table("ID", "Title", "Status", "URL")
    for row in rows:
        table.add_row(row["anime_id"], row["title"], row["status"], row["url"] or "")
    console.print(table)

@app.command()
def remove(anime_id: str):
    """Remove an anime from the watchlist."""
    console.print("[green]Removed.[/green]" if Database().remove(anime_id)
                  else "[yellow]Title not found.[/yellow]")

@app.command("play")
def play_command(target: str = typer.Argument(..., help="Local file or authorised HTTP(S) media URL.")):
    """Play a local or authorised media target with MPV."""
    try:
        code = play(target)
    except PlayerError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1) from exc
    if code:
        raise typer.Exit(code)

if __name__ == "__main__":
    app()
