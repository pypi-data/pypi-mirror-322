import json
from pathlib import Path
from kuzco.helpers.logger import get_logger
from kuzco.core.venv_manager import VenvManager

logger = get_logger(__name__)

class RunManager:
    def __init__(self, args):
        self.args = args
        self.venv_manager = VenvManager(args)

    def run_main(self):
        """
        Run the main.py script within the virtual environment with a decorator applied.
        """
        target_main_file = Path(self.args.get("target_service_main_file"))
        if not target_main_file.exists():
            raise FileNotFoundError(f"main.py file not found at {target_main_file}")

        if not self.venv_manager.venv_exists():
            raise EnvironmentError("Virtual environment does not exist. Please create it first.")

        # Discover all dependencies recursively
        all_dependencies = self._get_all_local_dependencies()
        self.args["all_dependencies"] = all_dependencies

        # Execute the script within the virtual environment
        try:
            logger.info(f"Running {target_main_file} in the virtual environment.")
            command = [
                "python",
                "-c",
                self._generate_decorator_script(target_main_file, all_dependencies)
            ]
            if self.args.get("docker") == "false":
                self.venv_manager.run_command_in_venv(command, echo=False)
            elif self.args.get("app_json_file"):
                self.venv_manager.run_global_command(command, echo=False)
        except Exception as e:
            logger.error(f"Failed to run {target_main_file}: {e}")
            raise
#################### shall be in different class
    def _get_all_local_dependencies(self):
        """
        Discover all local dependencies recursively by reading `local-utils.json` files.
        """
        visited = set()
        dependencies = []

        def read_dependencies(base_dir):
            local_utils_path = base_dir / "local-utils.json"
            if not local_utils_path.exists() or base_dir in visited:
                return
            visited.add(base_dir)

            try:
                with open(local_utils_path, "r") as file:
                    data = json.load(file)
                    local_dependencies = data.get("local_dependencies", [])
                    for dep in local_dependencies:
                        dep_dir = Path(self.args["mono_repo_base_dir"]) / "utils" / dep
                        if dep_dir.exists():
                            dependencies.append(dep)
                            read_dependencies(dep_dir)
            except Exception as e:
                logger.error(f"Failed to read dependencies from {local_utils_path}: {e}")

        # Start from the target service directory
        target_service_dir = Path(self.args["target_service_location"])
        read_dependencies(target_service_dir)

        return dependencies


    def _generate_decorator_script(self, target_main_file, all_dependencies):
        serialized_args = repr(self.args)
        utils_dir = repr(self.args.get("utils_dir"))
        uvicorn_args = self.args.get("uvicorn_args", {})

        script = f"""
import sys
import runpy
import uvicorn
from fastapi import FastAPI
from pathlib import Path

# Append only the directories of all_dependencies to the Python path
dependencies = {repr(all_dependencies)}
base_dir = {repr(self.args.get("mono_repo_base_dir"))}
for dep in dependencies:
    dep_path = str(Path(base_dir) / "utils" / dep / "app")
    if dep_path not in sys.path:
        sys.path.append(dep_path)

# Append the app_dir (where the target main file resides) to the Python path
app_dir = {repr(str(target_main_file.parent))}
if app_dir not in sys.path:
    sys.path.append(app_dir)

print("Updated sys.path:", sys.path)

def decorator(func, args, dependencies):
    def wrapper(*func_args, **func_kwargs):
        print("hello from decorator")
        print("RunManager args:", args)
        print("Service is dependent on:", dependencies)
        
        # Extract the FastAPI app from the main function
        app = func(*func_args, **func_kwargs)
        
        if isinstance(app, FastAPI):
            # Configure Uvicorn with the extra arguments
            uvicorn_config = {{
                "app": app,
                "host": "0.0.0.0",
                "port": 8000,
                "log_level": "info"
            }}
            uvicorn_config.update({uvicorn_args})
            
            # Run the Uvicorn server with the configured options
            uvicorn.run(**uvicorn_config)
        else:
            return app
    return wrapper

target_file = {repr(str(target_main_file))}
module_globals = runpy.run_path(target_file)

if 'main' in module_globals and callable(module_globals['main']):
    original_main = module_globals['main']
    decorated_main = decorator(original_main, {serialized_args}, {repr(all_dependencies)})
    decorated_main()
"""
        return script
