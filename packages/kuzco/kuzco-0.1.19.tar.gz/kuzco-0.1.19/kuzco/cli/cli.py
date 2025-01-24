import os
import json
import click
import subprocess
from pathlib import Path
from kuzco.core.case_manager import CaseManager
from kuzco.core.creator_manager import CreatorManager
from kuzco.scripts.tree import ProjectTreeBuilder
from kuzco.core.rundebug_manager import RunDebugConfigurationGenerator

# Validator for app name
def validate_app_name(ctx, param, value):
    if not value.islower() or not all(c.isalnum() or c in {'-'} for c in value):
        raise click.BadParameter("App name must be lowercase and can only contain letters, numbers, and '-'.")
    return value

@click.group()
def cli():
    """
    CLI tool for managing Python monorepos.
    """
    pass

@cli.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
@click.argument('command', type=click.Choice(['run', 'install', 'ci', 'restart'], case_sensitive=False))
@click.argument('type', type=click.Choice(['service', 'utils'], case_sensitive=False))
@click.argument('app_name', callback=validate_app_name)
@click.option('--docker', is_flag=True, help="Enable Docker support.")
@click.option('--uvicorn', is_flag=True, help="Enable Uvicorn with additional arguments.")
@click.pass_context
def manage(ctx, command, type, app_name, docker, uvicorn):
    """
    Manage monorepo services or utils.

    COMMAND: run/install/ci/restart
    TYPE: service/utils
    APP_NAME: Name of the application (lowercase, numbers, and '-' only).
    """
    # Hardcoded configuration
    config_data = {
        "repo_name": "src",
        "services_dir": "services",
        "utils_dir": "utils",
        "venv_dir_name": ".venv",
        "version_lock_file": "versions-lock.json",
        "service_main_file": "main.py",
        "local_utils_file": "local-utils.json"
    }

    config_path = os.getcwd()  # Use current working directory as the base
    mono_repo_base_dir = os.path.join(config_path, config_data["repo_name"])
    services_dir = os.path.join(mono_repo_base_dir, config_data["services_dir"])

    # Construct paths
    paths = {
        "project_base_dir": config_path,
        "mono_repo_base_dir": mono_repo_base_dir,
        "services_dir": services_dir,
        "utils_dir": os.path.join(mono_repo_base_dir, config_data["utils_dir"]),
        "target_service_location": os.path.join(services_dir, app_name),
        "target_service_venv_dir": os.path.join(services_dir, app_name, config_data["venv_dir_name"]),
        "target_service_main_file": os.path.join(services_dir, app_name, "app", config_data["service_main_file"]),
        "app_json_file": os.path.join(services_dir, app_name, config_data["local_utils_file"]),
        "docker_ignore_file": os.path.join(config_path, ".dockerignore"),
        "version_lock_file": os.path.join(mono_repo_base_dir, config_data["version_lock_file"])
    }
    required_paths = {
        "project_base_dir": config_path,
        "mono_repo_base_dir": mono_repo_base_dir,
        "services_dir": services_dir,
        "utils_dir": os.path.join(mono_repo_base_dir, config_data["utils_dir"]),
        "target_service_location": os.path.join(services_dir, app_name),
        "target_service_main_file": os.path.join(services_dir, app_name, "app", config_data["service_main_file"]),
        "app_json_file": os.path.join(services_dir, app_name, config_data["local_utils_file"]),
        "version_lock_file": os.path.join(mono_repo_base_dir, config_data["version_lock_file"])
    }

    for name, path in required_paths.items():
        if not os.path.exists(path):
            click.echo(f"Error: Required path '{name}' does not exist: {path}")
            return   

    extra_args_dict = {}
    if uvicorn:
        for arg in ctx.args:
            if arg.startswith("--"):
                if "=" not in arg:
                    click.echo(f"Error: Invalid argument format: {arg}. Must be in the form --key=value.")
                    return
                key, value = arg[2:].split('=', 1)
                extra_args_dict[key] = value

    monopylib_args = {
        'cli_current_command': command,
        'docker': str(docker).lower(),
        'uvicorn': str(uvicorn).lower(),
        'uvicorn_args': extra_args_dict,
        **paths
    }

    case_manager = CaseManager(monopylib_args)
    case_manager.execute()

@cli.group()
def create():
    """
    Create monorepo structures and files.
    """
    pass



@create.command()
@click.option('--base-path', default=".", show_default=True, type=click.Path(exists=True, file_okay=False), help="Base path for creating the monorepo.")
def monorepo(base_path):
    """
    Create a new monorepo structure.
    """
    port = None
    creator = CreatorManager(base_path)
    creator.create_monorepo()


@create.command()
@click.argument('service_name', callback=validate_app_name)
@click.argument('base_path', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--uvicorn', is_flag=True, default=False, help="Include uvicorn setup.")
@click.option('--port', default=8000, type=int, help="Port for uvicorn", required=False, is_eager=True)
def service(service_name, base_path, uvicorn, port):
    """
    Create a new service inside the monorepo.
    """
    if uvicorn and port:
        click.echo(f"Starting Uvicorn with port {port}")
        
    creator = CreatorManager(os.path.dirname(base_path))
    creator.create_service(service_name, port, uvicorn)



@create.command()
@click.argument('util_name')
@click.argument('base_path', type=click.Path(exists=True, dir_okay=True, file_okay=False))
def util(util_name, base_path):
    """
    Create a new utility inside the monorepo.
    """
    creator = CreatorManager(os.path.dirname(base_path))
    creator.create_util(util_name)

@create.command()
@click.argument('base_dir', default=".",  type=click.Path(exists=True, file_okay=False))
def rundebug(base_dir):
    """
    Generate RunDebug configurations for all services found in 'src/services'.
    """
    base_dir = os.path.abspath(base_dir)

    services_dir = os.path.join(base_dir, "src", "services")
    if not os.path.exists(services_dir):
        raise click.ClickException("Error: 'src/services' directory does not exist.")

    services_list = [
        d for d in os.listdir(services_dir)
        if os.path.isdir(os.path.join(services_dir, d))
    ]

    if not services_list:
        raise click.ClickException("Error: No services found in 'src/services'.")

    generator = RunDebugConfigurationGenerator(base_dir, services_list)
    generator.generate_all()

    click.echo(f"RunDebug configurations and scripts generated successfully for services: {', '.join(services_list)}")


@cli.group()
def tree():
    """
    Generate and display the project tree structure.
    """
    pass

@tree.command()
@click.argument('base_dir', type=click.Path(exists=True), default='.')
def show(base_dir):
    """
    Show the project tree structure based on the provided base directory.
    BASE_DIR: Path to the base directory of the project.
    """
    try:
        builder = ProjectTreeBuilder(base_dir)
        tree = builder.build_tree()
        click.echo(json.dumps(tree, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}")


@cli.group()
def ci():
    """CI related commands."""
    pass

@ci.command()
@click.argument('base_dir', default=".",  type=click.Path(exists=True, file_okay=False))
@click.option('--base', default="HEAD~1", help='Base commit hash (e.g., HEAD~1).')
@click.option('--head', default="HEAD", help='Head commit hash (e.g., HEAD).')
def list( base, head, base_dir):
    """
    List the services affected by changes between two git commits.

    --base-dir: Path to the base directory of the project.
    """
    try:
        # Step 1: Build the project tree
        builder = ProjectTreeBuilder(base_dir)
        project_tree = builder.build_tree()
        utils_to_services = builder.util_to_services
        
    #     # Step 2: Get git diff for the given range
        diff_result = get_git_diff(base, head, base_dir)   
        changed_services = set(diff_result['services'])
        changed_utils = set(diff_result['utils'])

        # Step 3: Determine affected services
        affected_services = set(changed_services)
        for util in changed_utils:
            if util in utils_to_services:
                affected_services.update(utils_to_services[util])

    #     # Step 4: Display affected services
        click.echo(json.dumps({"affected_services": sorted(affected_services)}, indent=2))

    except Exception as e:
        click.echo(f"Error: {e}")


def get_git_diff(base, head, base_path):
    diff = subprocess.check_output([
        'git', 'diff', '--name-only', '--diff-filter=ACMR', f'{base}..{head}', '--', base_path
    ]).decode().splitlines()
    services = set()
    utils = set()
    for file in diff:
        folders = file.split('/')   
        if len(folders) >= 4:  
            if folders[1] == 'services':
                services.add(folders[2])
            elif folders[1] == 'utils':
                utils.add(folders[2])    
    results = {'services': services, 'utils': utils}
    return results


if __name__ == '__main__':
    cli()