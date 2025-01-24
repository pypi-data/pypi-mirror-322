import json
import ast
import sys
from pathlib import Path
from kuzco.helpers.logger import get_logger
from kuzco.core.venv_manager import VenvManager

logger = get_logger(__name__)

class PipManager:
    def __init__(self, args):
        self.args = args
        self.venv_manager = VenvManager(args)
        self.visited_services = set()

    def install_dependencies(self):
        """Install dependencies for the target service and its local dependencies, then check imports."""
        target_service_location = Path(self.args.get("target_service_location"))
        app_json_file = Path(self.args.get("app_json_file"))
        
        if not app_json_file.exists():
            raise FileNotFoundError(f"App JSON file not found at {app_json_file}")

        dependencies = self._resolve_local_dependencies(app_json_file)
        combined_requirements = self._combine_requirements(target_service_location, dependencies)

        requirements_lock_path = target_service_location / "requirements-lock.txt"
        with open(requirements_lock_path, "w") as f:
            f.write("\n".join(combined_requirements))

        self._check_imports(target_service_location, dependencies)

        if self.args.get("docker") == "false":
            # Use virtual environment
            self.venv_manager.create_venv()
            self.venv_manager.activate_venv()
            logger.info(f"Installing dependencies from {requirements_lock_path}... on venv")
            self.venv_manager.run_pip_command(["install", "-r", str(requirements_lock_path)])
            logger.info("Dependencies installed on venv successfully.")
        elif self.args.get("app_json_file"):
            # Use global installation
            logger.info(f"Installing dependencies from {requirements_lock_path}... global")
            self.venv_manager.run_global_pip_command(["install", "-r", str(requirements_lock_path)])
            logger.info("Dependencies installed globally successfully.")

    def _resolve_local_dependencies(self, app_json_path):
        if not app_json_path.exists():
            raise FileNotFoundError(f"Local-utils.json not found at {app_json_path}")

        dependencies = []
        app_location = app_json_path.parent
        self.visited_services.add(app_location)

        with open(app_json_path, "r") as f:
            data = json.load(f)
        local_deps = data.get("local_dependencies", [])
        utils_dir = Path(self.args.get("utils_dir"))

        for dep in local_deps:
            dep_path = utils_dir / dep
            dep_json_file = dep_path / "local-utils.json"

            if not dep_path.exists():
                logger.error(f"Dependency '{dep}' does not exist at path: {dep_path}")
                raise SystemExit(1)

            if dep_path in self.visited_services:
                raise ValueError(f"Circular dependency detected with {dep_path}")

            if dep_json_file.exists():
                dependencies.append(dep_path)
                dependencies += self._resolve_local_dependencies(dep_json_file)
            else:
                logger.error(f"Dependency '{dep}' is missing its local-utils.json file at {dep_json_file}")
                raise SystemExit(1)

        return dependencies

    def _combine_requirements(self, target_service_location, dependencies):
        requirements = set()
        requirements_lock = self._read_version_lock()

        target_requirements = target_service_location / "requirements.txt"
        if target_requirements.exists():
            requirements.update(self._read_requirements_file(target_requirements))

        for dep in dependencies:
            dep_requirements = dep / "requirements.txt"
            if dep_requirements.exists():
                requirements.update(self._read_requirements_file(dep_requirements))

        resolved_requirements = self._apply_version_lock(requirements, requirements_lock)
        return sorted(resolved_requirements)

    def _read_requirements_file(self, path):
        with open(path, "r") as f:
            return {line.split("==")[0].strip() for line in f if line.strip() and not line.startswith("#")}

    def _read_version_lock(self):
        version_lock_file = Path(self.args.get("version_lock_file"))
        if not version_lock_file.exists():
            return {}

        try:
            with open(version_lock_file, "r") as f:
                data = json.load(f)
            common_requirements = data.get("common_requirements", [])
            return {
                requirement.split("==")[0].strip(): requirement.strip()
                for requirement in common_requirements
            }
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Error reading version-lock file: {e}")
            return {}

    def _apply_version_lock(self, requirements, version_lock):
        return {version_lock.get(req, req) for req in requirements}

    def _check_imports(self, target_service_location, dependencies):
        imports = self._collect_imports(target_service_location)
        for dep in dependencies:
            imports.update(self._collect_imports(dep))

        requirements_lock = self._read_requirements_lock(target_service_location)
        local_deps = self._get_local_dependencies(target_service_location)

        for dep in dependencies:
            local_deps.update(self._get_local_dependencies(dep))

        missing_imports = self._find_missing_imports(imports, requirements_lock, local_deps)

        if missing_imports:
            logger.error("Missing imports detected:")
            for imp in missing_imports:
                logger.error(f"- {imp}")
            sys.exit(1)
        else:
            logger.info("All imports are satisfied.")

    def _collect_imports(self, directory):
        imports = set()
        for file_path in directory.rglob("*.py"):
            if ".venv" not in str(file_path):
                with open(file_path, "r") as f:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports.add(alias.name.split(".")[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.level == 0:  # absolute import
                                imports.add(node.module.split(".")[0])
        return imports

    def _read_requirements_lock(self, target_service_location):
        requirements_lock_path = target_service_location / "requirements-lock.txt"
        if not requirements_lock_path.exists():
            return set()
        with open(requirements_lock_path, "r") as f:
            return {line.split("==")[0].strip() for line in f if line.strip() and not line.startswith("#")}

    def _get_local_dependencies(self, directory):
        app_json_file = directory / "local-utils.json"
        if not app_json_file.exists():
            return set()
        with open(app_json_file, "r") as f:
            data = json.load(f)
        return set(data.get("local_dependencies", []))

    def _find_missing_imports(self, imports, requirements, local_deps):
        standard_libs = set(sys.builtin_module_names)
        return imports - (requirements | local_deps | standard_libs)
