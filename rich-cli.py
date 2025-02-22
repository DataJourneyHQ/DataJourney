import click
import rich_click as rclick
import subprocess
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
    table = Table(title="Available tasks", show_lines=True)
    table.add_column("Workflow Name", style="bold cyan")
    table.add_column("Command", style="green")

    workflows = config.get("tasks", {})

    for name, details in workflows.items():
        table.add_row(name, details.get("cmd", "N/A"))

    console.print(table)

@cli.command()
@click.argument("tasks")
def run_workflow(workflow):
    """▶️ Run a Pixel.dev workflow from pixi.toml"""
    tasks = config.get("tasks", {})
    if task not in tasks:
        console.print(f"[red]Error:[/] Workflow [bold]{tasks}[/bold] not found!", style="bold red")
        return

    command = tasks[task].get("cmd", "")
    console.print(f"🚀 Running [bold cyan]{task}[/bold cyan]: {command}")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    console.print(f"[bold green]Output:[/bold green] {result.stdout}")
    if result.stderr:
        console.print(f"[bold red]Error:[/bold red] {result.stderr}")

if __name__ == "__main__":
    cli()
