import git
import typer
import importlib.util
import sys
from pathlib import Path

from rich.progress import Progress, SpinnerColumn, TextColumn

from blocks_cli.console import console
from blocks_cli.api import api_client
from blocks_cli.bundles import get_bundle_upload_url, upload_bundle_zip
from blocks_cli.config.config import config
from blocks_cli.commands.__base__ import blocks_cli
from blocks_cli.builds import poll_build_status
from blocks_cli.registration import get_blocks_state_and_module_from_file
from blocks_cli.package import warn_current_package_version

@blocks_cli.command()
def push(file: Path = typer.Argument(..., help="Name of blocks file to push.")):
    try:
        warn_current_package_version()

        # Create automation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as init_progress:
            init_task = init_progress.add_task(description="Initializing...", total=None)

            # working directory from where the command was invoked
            cwd = file.resolve().parent

            # parent folder name
            parent_folder_name = cwd.name

            git_remote_url = None

            try:
                repo = git.Repo(search_parent_directories=True)
                git_remote_url = repo.remotes.origin.url if repo.remotes else None
            except Exception as e:
                pass

            requirements_path = str((cwd / "requirements.txt").resolve())
            bundle_upload = get_bundle_upload_url()

            bundle_id = bundle_upload.get("bundle_id")
            bundle_upload_url = bundle_upload.get("bundle_upload_url")

            init_progress.update(
                init_task, total=1, description="Bundle uploaded successfully"
            )
            upload_bundle_zip(bundle_upload_url, cwd)
            init_progress.update(
                init_task, total=1, description="Bundle uploaded successfully"
            )

            # get pip dependencies

            pip_dependencies = []
            
            if Path(requirements_path).exists():
                with open(requirements_path, "r") as f:
                    pip_dependencies = f.read().splitlines()

            init_progress.update(
                init_task, total=1, description="Collecting automations..."
            )

            state, _ = get_blocks_state_and_module_from_file(file)

        # Construct payload
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as upload_progress:
            upload_task = upload_progress.add_task(
                description="Uploading automation...", total=None
            )

            registration_payload = {
                "git_remote_url": git_remote_url,
                "pip_dependencies": pip_dependencies,
                "bundle_id": bundle_id,
                "automations": [],
            }

            for automation in state.automations:
                trigger_kwargs = automation.get("trigger_kwargs", {})
                task_kwargs = automation.get("task_kwargs", {})

                automation_name = task_kwargs.get("name")
                vcpus = task_kwargs.get("vcpus", 1)
                memory_mib = task_kwargs.get("memory_mib", 1024)
                gpu_count = task_kwargs.get("gpu_count", 0)
                gpu_type = task_kwargs.get("gpu_type", "")

                repos: list = trigger_kwargs.get("repos", [])

                if len(repos) == 0 and git_remote_url:
                    repos.append(git_remote_url)

                function_name = automation.get("function_name")
                function_source_code = automation.get("function_source_code")
                trigger_alias = automation.get("trigger_alias")

                # Extract known fields
                automation_config = {
                    "name": automation_name,
                    "import_path": f"{parent_folder_name}/{file.name}:{function_name}",
                    "vcpus": vcpus,
                    "memory_mib": memory_mib,
                    "gpu_count": gpu_count,
                    "gpu_type": gpu_type,
                    "trigger_alias": trigger_alias,
                    "trigger_kwargs": {},
                    "task_kwargs": {},
                }

                # Add any additional args that weren't explicitly handled
                additional_task_kwargs = {
                    k: v
                    for k, v in trigger_kwargs.items()
                    if k not in ["vcpus", "memory_mib", "gpu_count", "gpu_type", "name"]
                }
                automation_config["trigger_kwargs"] = trigger_kwargs
                automation_config["task_kwargs"] = additional_task_kwargs
                registration_payload["automations"].append(automation_config)

        # Register automation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as registration_progress:
            registration_task = registration_progress.add_task(
                description="Registering automation...", total=None
            )
            res = api_client.post(
                f"{config.clients.client_url}/v1/register", json=registration_payload
            )
            # TODO add error handling
            res.raise_for_status()
            registration_progress.update(
                registration_task, total=1, description="Automation registered successfully"
            )

        # Verify build status
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as build_progress:
            build_task = build_progress.add_task(
                description="Building automation... This may take several minutes.",
                total=None,
            )
            build_id = res.json().get("build_id")
            image_id = res.json().get("image_id")
            is_build_triggered = res.json().get("is_build_triggered")
            if is_build_triggered:
                build_status = poll_build_status(image_id, build_id)
                build_progress.update(
                    build_task, total=1, description="Build completed successfully"
                )
    except Exception as e:
        console.print(f"[red] Error pushing automation: {str(e)}[/red]")
        raise typer.Exit(1)