#!/usr/bin/env python3
import argparse
import subprocess
import os
import time
import threading
import yaml
import requests


CONFIGURATION_FILE = "ms_configuration.yml"

class ServiceManager:
    def __init__(self,dir=None):
        self.base_dir = dir if dir else "./"
        self.services = {}
        self.threads = []

        if os.path.exists(CONFIGURATION_FILE):
            with open(CONFIGURATION_FILE, 'r') as file:
                self.services = yaml.safe_load(file)
        else:
            print(f"Configuration not fount!")

    def wait_for_dependency(self, port, thread_timeout=180):
        start_time = time.time()

        while time.time() - start_time < thread_timeout:
            try:
                url = f'http://localhost:{port}/actuator/health'
                response = requests.get(url, timeout=5)
                if response.status_code in [200, 503]:
                    return True
            except (requests.ConnectionError, requests.Timeout):
                time.sleep(5)

        return False

    def start_service(self, name, config):
        """Start a service on a separate thread"""

        # Wait for dependencies first
        for dependency in config.get('dependencies', []):
            dep_config = self.services.get(dependency)
            if not dep_config:
                continue

            print(f"Waiting for {dependency} to be ready...")
            if not self.wait_for_dependency(dep_config['port']):
                print(f"Timeout waiting for {dependency}. Aborting {name}.")
                return

        print(f"Starting {name}...")
        service_dir = os.path.join(self.base_dir, config["path"])

        if not os.path.isdir(service_dir):
            print(f"Error: Path not found: {service_dir}")
            return

        try:
            os.chdir(service_dir)
            command = "skaffold dev --port-forward"
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error on starting {name}: {e}")
        except Exception as e:
            print(f"Error on {name}: {e}")

    def start_all(self):
        """Start all enabled services"""
        original_dir = os.getcwd()

        for name, config in self.services.items():
            if config.get("enabled", True):
                thread = threading.Thread(
                    target=self.start_service,
                    args=(name, config),
                    daemon=True
                )
                self.threads.append(thread)
                thread.start()
            else:
                print(f"{name} disabled, skiping...")

        try:
            for thread in self.threads:
                thread.join()
        except KeyboardInterrupt:
            print("\nStoping services...")
        finally:
            os.chdir(original_dir)

    def save_config(self, args, filename=CONFIGURATION_FILE):
        # Update configuration
        if args.disable:
            for service in args.disable:
                if service in self.services:
                    self.services[service]["enabled"] = False

        if args.enable:
            for service in args.enable:
                if service in self.services:
                    self.services[service]["enabled"] = True

        if args.save:
            with open(filename, 'w') as file:
                yaml.dump(self.services, file, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description="Microservices Local Manager")
    parser.add_argument("--dir", "-d", default="./", help="Microservices base path")
    parser.add_argument("--disable", nargs="+", help="Services to disable")
    parser.add_argument("--enable", nargs="+", help="Services to enable")
    parser.add_argument("--save", action="store_true", help="Save coonfiguration to YML")
    args = parser.parse_args()

    subprocess.run("clear", shell=True, check=True)
    manager = ServiceManager(args.dir)
    manager.save_config(args)
    manager.start_all()


if __name__ == "__main__":
    main()