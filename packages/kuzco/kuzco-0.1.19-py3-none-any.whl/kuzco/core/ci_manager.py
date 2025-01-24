import os
import json

class CIManager:
    def __init__(self, args):
        self.args = args
        self.base_dir = args.get("mono_repo_base_dir")
        self.target_service = args.get("target_service_location")
        self.docker_ignore_file = args.get("docker_ignore_file")
        self.utils_dir = os.path.join(self.base_dir, "utils")
        self.services_dir = os.path.join(self.base_dir, "services")

    def generate_dockerignore(self):
        """Generate a .dockerignore file based on best practices and dependencies."""
        # Ensure the directory for the .dockerignore file exists
        dockerignore_dir = os.path.dirname(self.docker_ignore_file)
        if not os.path.exists(dockerignore_dir):
            os.makedirs(dockerignore_dir)

        ignore_patterns = self.get_default_ignore_patterns()

        # Add service-specific ignore rules
        service_name = os.path.basename(self.target_service)
        ignore_patterns += self.get_service_ignore_patterns(service_name)

        # Write or overwrite the .dockerignore file
        with open(self.docker_ignore_file, "w") as dockerignore:
            dockerignore.write("\n".join(ignore_patterns))

        print(f".dockerignore generated at: {self.docker_ignore_file}")

    def get_default_ignore_patterns(self):
        """Return default ignore patterns for Python projects."""
        return [
            "*.pyc",
            "__pycache__/",
            ".venv/",
            ".mypy_cache/",
            ".pytest_cache/",
            ".coverage",
            ".DS_Store",
            "*.egg-info/",
            "build/",
            "dist/",
            "*.log",
            "requirements-lock.txt"
        ]

    def get_service_ignore_patterns(self, target_service_name):
        """Return ignore patterns for services and utils excluding dependencies."""
        # Ignore all other services except the target
        service_dirs = [d for d in os.listdir(self.services_dir) if os.path.isdir(os.path.join(self.services_dir, d))]
        ignore_services = [f"src/services/{s}" for s in service_dirs if s != target_service_name]

        # Resolve utility dependencies
        dependencies = self.resolve_dependencies()

        # Ignore all other utils except the resolved dependencies
        util_dirs = [d for d in os.listdir(self.utils_dir) if os.path.isdir(os.path.join(self.utils_dir, d))]
        ignore_utils = [f"src/utils/{u}" for u in util_dirs if u not in dependencies]

        return ignore_services + ignore_utils

    def resolve_dependencies(self):
        """Resolve recursive dependencies for the target service."""
        resolved = set()
        to_process = [os.path.basename(self.target_service)]

        while to_process:
            current = to_process.pop()
            if current in resolved:
                continue

            resolved.add(current)
            local_utils_file = os.path.join(
                self.services_dir if current in os.listdir(self.services_dir) else self.utils_dir,
                current,
                "local-utils.json"
            )

            if os.path.exists(local_utils_file):
                with open(local_utils_file, "r") as f:
                    data = json.load(f)
                    dependencies = data.get("local_dependencies", [])
                    to_process.extend(dependencies)

        return resolved