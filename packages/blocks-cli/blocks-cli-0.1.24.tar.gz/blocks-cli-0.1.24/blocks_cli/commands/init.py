import git
import typer
from pathlib import Path

from rich.progress import Progress, SpinnerColumn, TextColumn

from blocks_cli.api import api_client
from blocks_cli.commands.__base__ import blocks_cli
from blocks_cli.package import warn_current_package_version
from blocks_cli.config.config import config
from blocks_cli.console import console

@blocks_cli.command()
def init(apikey: str = typer.Option(None, "--key", help="API key for authentication")):
    """Initialize blocks in the current directory."""
    try:
        warn_current_package_version()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as progress:

            working_dir = Path.cwd()
            try:
                repo = git.Repo(search_parent_directories=True)
                working_dir = repo.working_dir
            except Exception as e:
                pass

            working_dir = Path(working_dir)

            # Create .blocks directory if it doesn't exist
            blocks_dir = working_dir / ".blocks"

            if not blocks_dir.exists():
                blocks_dir.mkdir()
                folder_task = progress.add_task(description="Creating .blocks folder...", total=None)
                progress.update(folder_task, description="[green]Created .blocks folder[/green]")

            progress.refresh()

            # Verify and save API key if provided
            if apikey:
                api_task = progress.add_task(description="Verifying API key...", total=None)

                response = api_client.get(f"{config.clients.client_url}/v1/apikeys/{apikey}", headers={
                    "Authorization": f"ApiKey {apikey}"
                })

                if response.status_code > 299:
                    raise Exception("API Key is invalid. Please check your API key at [link=https://app.blocksorg.com]https://app.blocksorg.com[/link]")
                
                config.auth.save_api_key(apikey)
                progress.update(api_task, description="[green]API key verified and saved successfully[/green]")
                progress.refresh()

        console.print("[green]Blocks has been successfully initialized.[/green]")

    except Exception as e:
        console.print(f"[red]Error initializing blocks: {str(e)}[/red]")
        raise typer.Exit(code=1)
