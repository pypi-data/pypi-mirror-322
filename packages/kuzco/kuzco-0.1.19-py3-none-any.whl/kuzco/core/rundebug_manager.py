import os
import xml.etree.ElementTree as ET


class RunDebugConfigurationGenerator:
    def __init__(self, base_dir, services_list):
        self.base_dir = base_dir
        self.services_list = services_list
        self.run_config_dir = os.path.join(base_dir, ".idea/runConfigurations")
        self.scripts_dir = os.path.join(base_dir, "src/scripts/bin")
        self.ensure_directories_exist()

    def ensure_directories_exist(self):
        os.makedirs(self.run_config_dir, exist_ok=True)
        os.makedirs(self.scripts_dir, exist_ok=True)

    def generate_run_configuration(self, name, script_path, parameters=None):
        config_path = os.path.join(self.run_config_dir, f"{name}.xml")
        if os.path.exists(config_path):
            return 
        base_dir_name = os.path.basename(self.base_dir)  # Extract the base directory name

        config = ET.Element("component", name="ProjectRunConfigurationManager")
        configuration = ET.SubElement(config, "configuration", {
            "default": "false",
            "name": name,
            "type": "PythonConfigurationType",
            "factoryName": "Python",
            "singleton": "true"
        })
        ET.SubElement(configuration, "module", name=base_dir_name)
        ET.SubElement(configuration, "option", name="SCRIPT_NAME", value=script_path)
        ET.SubElement(configuration, "option", name="WORKING_DIRECTORY", value="$PROJECT_DIR$")
        ET.SubElement(configuration, "option", name="EMULATE_TERMINAL", value="true")
        if parameters:
            ET.SubElement(configuration, "option", name="PARAMETERS", value=parameters)
        ET.SubElement(configuration, "method", v="2")

        tree = ET.ElementTree(config)
        with open(config_path, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

    def generate_python_script(self, script_name, command, interactive=False):
        script_path = os.path.join(self.scripts_dir, f"{script_name}.py")
        if os.path.exists(script_path):
            return  

        if "uvicorn" in command and not script_name.startswith("create_"):
            service_name = self._extract_service_name(script_name)
            action = "run" if "run" in script_name else "restart"
            script_content = f"""#!/usr/bin/env python3
import subprocess
import os

def load_env_file(env_file_path):
    env_vars = {{}}
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = map(str.strip, line.split('=', 1))
                    env_vars[key] = value
    return env_vars

env_file_path = os.path.join(os.path.dirname(__file__), '../../services/{service_name}/.env')
env_vars = load_env_file(env_file_path)
port = env_vars.get('PORT', '8000')

subprocess.run(['kuzco', 'manage', '{action}', 'service', '{service_name}', '.', '--uvicorn', f'--port={{port}}'], check=True)
"""
        elif interactive:
            target = "service" if "service" in script_name else "util"
            if script_name == "create_uvicorn_service":
                script_content = f"""#!/usr/bin/env python3
import subprocess

input_value = input("Enter the name for the {target}: ")
port = input("Enter the port number (e.g., 3000): ")
command = {command}
command.insert(-2, input_value)
command.append(f'--port={{port}}')
subprocess.run(command, check=True)
"""
            else:
                script_content = f"""#!/usr/bin/env python3
import subprocess

input_value = input("Enter the name for the {target}: ")
command = {command}
command.insert(-1, input_value)
subprocess.run(command, check=True)
"""
        else:
            script_content = f"""#!/usr/bin/env python3
import subprocess

subprocess.run({command}, check=True)
"""

        with open(script_path, "w") as f:
            f.write(script_content)


    def _extract_service_name(self, file_name):
        if file_name.startswith("run_service_") or file_name.startswith("restart_service_"):
            parts = file_name.split("_")
            return parts[2] if len(parts) > 2 else None
        return None

    def generate_static_rundebug_configuration(self):
        static_name = "refresh-rundebug"
        static_script_name = "refresh_rundebug"
        static_command = ["kuzco", "create", "rundebug", "."]

        self.generate_python_script(static_script_name, repr(static_command))
        self.generate_run_configuration(
            static_name,
            os.path.join(self.scripts_dir, f"{static_script_name}.py")
        )

    def generate_all(self):
        for service_name in self.services_list:
            commands = {
                f"run-service-{service_name}": ["kuzco", "manage", "run", "service", service_name, "."],
                f"run-service-{service_name}-uvicorn": ["kuzco", "manage", "run", "service", service_name, ".", "--uvicorn"],
                f"install-requirements-service-{service_name}": ["kuzco", "manage", "install", "service", service_name, "."],
                f"generate-dockerignore-service-{service_name}": ["kuzco", "manage", "ci", "service", service_name, "."],
                f"restart-service-{service_name}": ["kuzco", "manage", "restart", "service", service_name, "."],
                f"restart-service-{service_name}-uvicorn": ["kuzco", "manage", "restart", "service", service_name, ".", "--uvicorn"],
                f"docker-build-service-{service_name}": ["docker", "build", "-f", f"src/services/{service_name}/Dockerfile", "-t", service_name, "."],
                f"docker-run-service-{service_name}": ["docker", "run", "--rm", "-p 8000:3000", service_name],
            }

            for name, command in commands.items():
                script_name = name.replace("-", "_")
                script_path = os.path.join(self.scripts_dir, f"{script_name}.py")
                self.generate_python_script(script_name, repr(command))
                self.generate_run_configuration(name, script_path)

        interactive_commands = {
            "create-service": ["kuzco", "create", "service", "."],
            "create-util": ["kuzco", "create", "util", "."],
            "create-uvicorn-service": ["kuzco", "create", "service", ".", "--uvicorn"],
        }

        for name, command in interactive_commands.items():
            script_name = name.replace("-", "_")
            interactive = True 
            self.generate_python_script(script_name, repr(command), interactive=interactive)
            self.generate_run_configuration(name, os.path.join(self.scripts_dir, f"{script_name}.py"))

        self.generate_static_rundebug_configuration()
