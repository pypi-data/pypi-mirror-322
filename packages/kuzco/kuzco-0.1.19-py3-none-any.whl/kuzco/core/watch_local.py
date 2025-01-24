#!/usr/bin/env python3
import os
import sys
import logging
import subprocess
import json
from signal import signal, SIGINT, SIGTERM
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style, init
import psutil

# Initialize colorama for cross-platform color support
init(autoreset=True)


class CustomFormatter(logging.Formatter):
    """Custom logging formatter with color support for different log levels."""
    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        level_color = self.LEVEL_COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{level_color}{message}{Style.RESET_ALL}"


class WatchLocal:
    def __init__(self, service_dir, command, env_file_path, port_env_var="PORT", default_port=8000):
        self.service_dir = service_dir
        self.command = command
        self.env_file_path = env_file_path
        self.port_env_var = port_env_var
        self.default_port = default_port
        self.logger = self.setup_logger()
        self.port = self.load_port()
        self.observer = None
        self.event_handler = None
        self.watched_paths = self.get_watched_paths()

    def setup_logger(self):
        """Setup a logger with a custom formatter."""
        logger = logging.getLogger("WatchLocal")
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = CustomFormatter(
            fmt=f"{Fore.BLUE}[%(asctime)s]{Style.RESET_ALL} %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def load_env_file(self):
        """Load environment variables from a .env file."""
        env_vars = {}
        if os.path.exists(self.env_file_path):
            self.logger.info(f"Loading environment variables from: {self.env_file_path}")
            with open(self.env_file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = map(str.strip, line.split('=', 1))
                        env_vars[key] = value
        else:
            self.logger.warning(f".env file not found at: {self.env_file_path}")
        return env_vars

    def load_port(self):
        """Load the port from environment variables or use the default."""
        env_vars = self.load_env_file()
        return int(env_vars.get(self.port_env_var, self.default_port))

    def free_port(self, port):
        """Check if a port is in use and terminate the process using it."""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for conn in proc.net_connections(kind='inet'):
                    if conn.laddr.port == port:
                        self.logger.warning(
                            f"Port {port} is in use by process {proc.info['name']} (PID: {proc.info['pid']}). Terminating it.")
                        proc.terminate()
                        proc.wait(timeout=5)
                        self.logger.info(
                            f"Terminated process {proc.info['name']} (PID: {proc.info['pid']}) using port {port}.")
                        return
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        self.logger.info(f"Port {port} is free.")

    def get_watched_paths(self):
        """Resolve all paths to be watched based on local-utils.json."""
        watched_paths = [os.path.join(self.service_dir, "app")]
        visited = set()

        def resolve_dependencies(current_path):
            if current_path in visited:
                return
            visited.add(current_path)

            json_path = os.path.join(current_path, "local-utils.json")
            if not os.path.exists(json_path):
                return

            try:
                with open(json_path, "r") as file:
                    data = json.load(file)
                    dependencies = data.get("local_dependencies", [])
                    for dep in dependencies:
                        dep_path = os.path.abspath(os.path.join(self.service_dir, "../../utils", dep))
                        app_path = os.path.join(dep_path, "app")
                        if os.path.exists(app_path):
                            watched_paths.append(app_path)
                        resolve_dependencies(dep_path)
            except Exception as e:
                self.logger.error(f"Error reading dependencies from {json_path}: {e}")

        resolve_dependencies(os.path.abspath(self.service_dir))
        self.logger.info(f"Watching paths: {watched_paths}")
        return watched_paths

    class ChangeHandler(FileSystemEventHandler):
        def __init__(self, command, port, logger, free_port_func):
            self.command = command
            self.port = port
            self.logger = logger
            self.free_port_func = free_port_func
            self.process = None
            self.run_command()

        def run_command(self):
            """Start or restart the service process."""
            if self.process and self.process.poll() is None:
                self.logger.info("Stopping the running process...")
                self.process.terminate()
                self.process.wait()

            # Free the port before starting a new process
            self.free_port_func(self.port)

            try:
                self.logger.info(f"Starting process: {' '.join(self.command)}")
                self.process = subprocess.Popen(self.command)
            except Exception as e:
                self.logger.error(f"Failed to start process: {e}")

        def on_any_event(self, event):
            """Trigger on any file change event."""
            if not event.is_directory:
                self.logger.info(f"Change detected: {event.src_path}")
                self.run_command()

        def cleanup(self):
            """Terminate the process if it's still running."""
            if self.process and self.process.poll() is None:
                self.logger.info("Cleaning up process...")
                self.process.terminate()
                self.process.wait()

    def start(self):
        """Start watching for file changes and running the service."""
        self.event_handler = self.ChangeHandler(self.command, self.port, self.logger, self.free_port)
        self.observer = Observer()
        for path in self.watched_paths:
            self.observer.schedule(self.event_handler, path=path, recursive=True)

        def shutdown_handler(signal_received, frame):
            """Handle graceful shutdown."""
            self.logger.info("\nShutting down...")
            self.observer.stop()
            self.event_handler.cleanup()
            self.observer.join()
            self.logger.info("Shutdown complete.")
            sys.exit(0)

        # Register signal handlers
        signal(SIGINT, shutdown_handler)
        signal(SIGTERM, shutdown_handler)

        try:
            self.logger.info(f"Watching for changes in: {self.watched_paths}")
            self.logger.info(f"Service will run on port: {self.port}")
            self.observer.start()
            self.observer.join()
        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            shutdown_handler(SIGTERM, None)


if __name__ == '__main__':
    # Define paths and commands
    env_file_path = os.path.join(os.path.dirname(__file__), '../../services/x/.env')
    service_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../services/x'))
    command = ['kuzco', 'manage', 'run', 'service', 'x', '.', '--uvicorn', '--port=8000']

    # Create and start WatchLocal instance
    watcher = WatchLocal(service_dir, command, env_file_path)
    watcher.start()
