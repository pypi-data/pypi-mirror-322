from kuzco.core.venv_manager import VenvManager
from kuzco.core.run_manager import RunManager
from kuzco.core.pip_manager import PipManager
from kuzco.core.ci_manager import CIManager
from kuzco.helpers.logger import get_logger


logger = get_logger(__name__)

class CaseManager:
    def __init__(self, args):
        self.args = args
        self.venv_manager = VenvManager(args)
        self.pip_manager = PipManager(args)
        self.ci_manager = CIManager(args)
        self.run_manager = RunManager(args)


    def execute(self):
        command = self.args.get("cli_current_command")
        if command == "run":
            self.run_service()
        elif command == "ci":
            self.run_ci()
        elif command == "install":
            self.install_dependencies()
        elif command == "restart":
            self.restart_service()
        else:
            print(f"Unknown command: {command}")

    def run_service(self):
        print("Executing 'run' command.")
        try:
            self.run_manager.run_main()
        except Exception as e:
            print(f"Error running the service: {e}")


    def run_ci(self):
        print("Executing 'ci' command.")
        try:
            self.ci_manager.generate_dockerignore()
        except Exception as e:
            print(f"Error performing ci step on service: {e}")


    def install_dependencies(self):
        print("Executing 'install' command.")
        try:
            self.pip_manager.install_dependencies()
        except Exception as e:
            print(f"Error install depndencies for service: {e}")

    def restart_service(self):
        try:
            self.pip_manager.install_dependencies()
            self.run_manager.run_main()
        except Exception as e:
            print(f"Error install depndencies for service: {e}")
