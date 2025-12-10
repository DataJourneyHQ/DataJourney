import click
import rich_click as rclick
from rich.table import Table
from rich.console import Console
import tomlkit

rclick.rich_click.USE_RICH_MARKUP = True  # Enable rich formatting
console = Console()

def read_pixi_toml():
    with open("pixi.toml", "r") as f:
        return tomlkit.parse(f.read())

config = read_pixi_toml()

@click.group()
def cli():
    """🚀 CLI for Managing Pixel.dev Workflows"""
    pass

@cli.command()
def list_workflows():
    """📜 Show available workflows in pixi.toml"""
    table = Table(title="🚀 Available Workflows under DataJourney", show_lines=True, header_style="bold magenta")

    table.add_column("🔹 Task Name", style="bold cyan", justify="left")
    table.add_column("📁 Source", style="bold green", justify="left")

    workflows = config.get("tasks", {})

    if not workflows:
        table.add_row("[dim]No workflows found[/dim]", "[dim]N/A[/dim]")
    else:
        for name, details in workflows.items():
            path = details.get("cwd", "[dim]N/A[/dim]")
            table.add_row(f"[bold]{name}[/bold]", path)

    console.print(table)

if __name__ == "__main__":
    list_workflows()
