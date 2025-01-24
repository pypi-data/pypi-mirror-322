import sys
import os
import platform
import subprocess
from pathlib import Path
from kuzco.helpers.logger import get_logger

logger = get_logger(__name__)

class VenvManager:
    def __init__(self, args):
        """
        Initialize the VenvManager with the path to the virtual environment.
        :param venv_path: Path to the virtual environment.
        """
        self.args = args
        self.venv_path = Path(self.args.get("target_service_venv_dir"))

    def venv_exists(self):
        """
        Check if the virtual environment already exists.
        :return: True if the virtual environment exists, False otherwise.
        """
        exists = self.venv_path.exists() and (self.venv_path / "bin").exists() or (self.venv_path / "Scripts").exists()
        logger.debug(f"Virtual environment exists: {exists}")
        return exists

    def create_venv(self):
        """
        Create the virtual environment if it doesn't exist.
        """
        if not self.venv_exists():
            try:
                logger.info(f"Creating virtual environment at {self.venv_path}...")
                subprocess.check_call(["python", "-m", "venv", str(self.venv_path)])
                logger.info("Virtual environment created successfully.")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to create virtual environment: {e}")
                raise

    def activate_venv(self):
        """
        Activate the virtual environment based on the operating system.
        :return: Path to the activation script for the virtual environment.
        """
        if not self.venv_exists():
            raise EnvironmentError("Virtual environment does not exist. Please create it first.")

        activate_script = None
        if platform.system() == "Windows":
            activate_script = self.venv_path / "Scripts" / "activate.bat"
        else:
            activate_script = self.venv_path / "bin" / "activate"

        if not activate_script.exists():
            raise FileNotFoundError(f"Activation script not found at {activate_script}")

        logger.debug(f"Activation script found at: {activate_script}")
        return activate_script

    def detect_platform(self):
        """
        Detect the current operating system.
        :return: String indicating the operating system (e.g., "Windows" or "Linux").
        """
        os_name = platform.system()
        logger.debug(f"Detected platform: {os_name}")
        return os_name
    
                        ########################################
                        #########                      #########
                        #########       RUN IN VENV    #########
                        #########                      #########
                        ########################################

    def run_command_in_venv(self, command, echo=True):
        """
        Run a command within the virtual environment using its Python executable.
        :param command: Command to run as a list (e.g., ["python", "app.py"]).
        :param echo: Whether to log the command being executed.
        """
        if not self.venv_exists():
            raise EnvironmentError("Virtual environment does not exist. Please create it first.")

        # Use the Python executable from the virtual environment
        python_executable = (
            self.venv_path / "Scripts" / "python.exe" if platform.system() == "Windows" else self.venv_path / "bin" / "python"
        )
        
        if not python_executable.exists():
            raise FileNotFoundError(f"Python executable not found in the virtual environment: {python_executable}")

        try:
            # Optionally log the command
            if echo:
                logger.info(f"Running command in virtual environment using {python_executable}: {' '.join(command)}")
            
            # Insert the Python executable at the beginning of the command
            full_command = [str(python_executable)] + command[1:]

            process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Stream output and errors
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()

            for line in process.stderr:
                sys.stderr.write(line)
                sys.stderr.flush()

            process.wait()
            if process.returncode != 0:
                logger.error(f"Command failed with return code {process.returncode}")
                raise subprocess.CalledProcessError(process.returncode, full_command)
            else:
                logger.info("Command executed successfully.")
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise


    def get_python_path(self):
        """
        Get the path to the Python executable within the virtual environment.
        :return: Path to the virtual environment's Python executable.
        """
        venv_dir = Path(self.args.get("target_service_venv_dir"))
        if not venv_dir.exists():
            raise EnvironmentError("Virtual environment does not exist.")

        # Check for the Python executable based on the platform
        if os.name == "nt":  # Windows
            python_executable = venv_dir / "Scripts" / "python.exe"
        else:  # Unix-based
            python_executable = venv_dir / "bin" / "python"

        if not python_executable.exists():
            raise EnvironmentError(f"Python executable not found in the virtual environment at {python_executable}.")
        
        return str(python_executable)



    def run_pip_command(self, command, echo=True):
        """
        Run a pip command within the virtual environment using its Python executable.
        :param command: Command to run as a list (e.g., ["install", "boto3"]).
        :param echo: Whether to log the command being executed.
        """
        if not self.venv_exists():
            raise EnvironmentError("Virtual environment does not exist. Please create it first.")

        python_executable = self.get_python_path()
        pip_command = [python_executable, "-m", "pip"] + command

        try:
            if echo:
                logger.info(f"Running pip command: {' '.join(pip_command)}")
            subprocess.check_call(pip_command)
        except subprocess.CalledProcessError as e:
            logger.error(f"Pip command failed: {e}")
            raise

                        ########################################
                        #########                      #########
                        #########       RUN GLOBAL     #########
                        #########                      #########
                        ########################################

    def run_global_command(self, command, echo=True):
        """
        Run a command globally using the system's Python or other executables.
        :param command: Command to run as a list (e.g., ["python", "script.py"]).
        :param echo: Whether to log the command being executed.
        """
        try:
            if echo:
                logger.info(f"Running global command: {' '.join(command)}")
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Stream output and errors
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()

            for line in process.stderr:
                sys.stderr.write(line)
                sys.stderr.flush()

            process.wait()
            if process.returncode != 0:
                logger.error(f"Global command failed with return code {process.returncode}")
                raise subprocess.CalledProcessError(process.returncode, command)
            else:
                logger.info("Global command executed successfully.")
        except Exception as e:
            logger.error(f"Global command execution failed: {e}")
            raise

    def run_global_pip_command(self, command, echo=True):
        """
        Run a pip command globally using the system's pip.
        :param command: Pip command to run as a list (e.g., ["install", "boto3"]).
        :param echo: Whether to log the command being executed.
        """
        try:
            # Use system's Python to call pip
            pip_command = ["python", "-m", "pip"] + command
            if echo:
                logger.info(f"Running global pip command: {' '.join(pip_command)}")
            
            subprocess.check_call(pip_command)
        except subprocess.CalledProcessError as e:
            logger.error(f"Global pip command failed: {e}")
            raise