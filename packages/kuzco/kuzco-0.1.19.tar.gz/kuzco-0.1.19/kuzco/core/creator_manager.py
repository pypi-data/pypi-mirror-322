import os
import json
import socket

class CreatorManager:
    def __init__(self, base_path):
        self.base_path = os.path.abspath(base_path)
        self.config = {
            "repo_name": "src",
            "services_dir": "services",
            "utils_dir": "utils",
            "venv_dir_name": ".venv",
            "version_lock_file": "versions-lock.json",
            "service_main_file": "main.py",
            "local_utils_file": "local-utils.json",
        }

    def create_monorepo(self):
        repo_name = "src"
        repo_path = os.path.join(self.base_path, repo_name)

        # Create main repo folder and subfolders
        os.makedirs(os.path.join(repo_path, "services"), exist_ok=True)
        os.makedirs(os.path.join(repo_path, "utils"), exist_ok=True)

        # Create README.md in the base path
        readme_path = os.path.join(self.base_path, "README.md")
        with open(readme_path, "w") as readme_file:
            readme_file.write(f"# {repo_name}\n\nWelcome to the {repo_name} monorepo!")

        # Create versions-lock.json inside the repo_name folder
        version_lock_path = os.path.join(repo_path, "versions-lock.json")
        version_lock_data = {"common_requirements": ["some-pip-package==x.y.z"]}
        self._write_json(version_lock_path, version_lock_data)

        print(f"Monorepo '{repo_name}' created at {repo_path}")

    def create_service(self, service_name, port, uvicorn=False):
        repo_path = os.path.join(self.base_path, self.config["repo_name"])
        service_path = os.path.join(repo_path, self.config["services_dir"], service_name)
        os.makedirs(service_path, exist_ok=True)
        os.makedirs(os.path.join(service_path, "app"), exist_ok=True)

        # Create Dockerfile
        dockerfile_content = self._generate_dockerfile(service_name, uvicorn)
        self._write_file(os.path.join(service_path, "Dockerfile"), dockerfile_content)

        # Create __init__.py
        self._write_file(os.path.join(service_path, "app", "__init__.py"), "")

        # Create main.py
        main_py_content = self._generate_main_py_content(service_name, uvicorn)
        self._write_file(os.path.join(service_path, "app", "main.py"), main_py_content)

        # Create local-utils.json
        self._write_json(
            os.path.join(service_path, self.config["local_utils_file"]),
            {"local_dependencies": []},
        )

        # Create requirements.txt
        requirements_content = "fastapi\nuvicorn" if uvicorn else ""
        self._write_file(os.path.join(service_path, "requirements.txt"), requirements_content)

        # Create .env file
        self._generate_env_file(service_path, uvicorn)

        print(f"Service '{service_name}' created at {port}")

    def create_util(self, util_name):
        repo_path = os.path.join(self.base_path, self.config["repo_name"])
        util_path = os.path.join(repo_path, self.config["utils_dir"], util_name)
        os.makedirs(util_path, exist_ok=True)
        os.makedirs(os.path.join(util_path, "app"), exist_ok=True)

        # Create __init__.py
        self._write_file(os.path.join(util_path, "app", "__init__.py"), "")

        # Create <util-name>.py
        util_content = self._generate_util_py_content(util_name)
        self._write_file(
            os.path.join(util_path, "app", f"{util_name}.py"), util_content
        )

        # Create local-utils.json
        self._write_json(
            os.path.join(util_path, self.config["local_utils_file"]),
            {"local_dependencies": []},
        )

        # Create requirements.txt
        self._write_file(os.path.join(util_path, "requirements.txt"), "")

        print(f"Utility '{util_name}' created at {util_path}")

    def _generate_dockerfile(self, service_name, uvicorn):
        base_dockerfile = f"""FROM python:3.11-slim

WORKDIR /app/src/services/{service_name}

COPY . /app

RUN pip install --upgrade kuzco

RUN kuzco manage install service {service_name} ../../.. --docker

EXPOSE 3000
"""
        cmd = (
            f'CMD ["kuzco", "manage", "run", "service", "{service_name}", "../../..", "--docker", "--uvicorn", "--port=3000"]'
            if uvicorn
            else f'CMD ["kuzco", "manage", "run", "service", "{service_name}", "../../..", "--docker"]'
        )
        return base_dockerfile + cmd

    def _generate_main_py_content(self, service_name, uvicorn):
        if uvicorn:
            return f"""from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {{"message": "Hello, {service_name} FastAPI!"}}

    
def main():
    return app

# the uvicorn implementation will  provide by kuzco

if __name__ == "__main__":
    main()
"""
        return f"""# from <some-local-util> import <some-util-function>

def main():
    # name = "BARAKUNI"
    # util_implementation_result = <some-util-function>(name)  
    # print(util_implementation_result)  
    print("Hello from service {service_name}")


if __name__ == "__main__":
    main()
"""

    def _generate_util_py_content(self, util_name):
        return f"""# from <some-other-local-util> import <some-other-util-function>

def {util_name}_functionallity(name: str) -> str:
    # <some-other-util-function>_result = <some-other-util-function>(name)
    # print(f"i am depends on <some-other-local-util>: <some-other-util-function>_result")
    return f"Hello, {{name}}! Welcome to the module {util_name}."

if __name__ == "__main__":
    print({util_name}_functionallity("Developer"))
"""

    def _generate_env_file(self, service_path, uvicorn):
        env_path = os.path.join(service_path, ".env")

        if uvicorn:
            with open(env_path, "w") as env_file:
                env_file.write(f"PORT={self.port}\n")
        else:
            with open(env_path, "w") as env_file:
                env_file.write("")

    def _find_available_port(self, start_port=8000, end_port=9000):
        for port in range(start_port, end_port):
            if not self._is_port_in_use(port):
                return port
        raise RuntimeError("No available ports in the specified range.")

    def _is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0

    def _write_json(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def _write_file(self, path, content):
        with open(path, "w") as f:
            f.write(content)
