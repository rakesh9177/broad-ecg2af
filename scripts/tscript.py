import os
import socket
import subprocess
from datetime import datetime

def track_and_push():
    try:
        # Step 1: Collect tracking information
        hostname = socket.gethostname()
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        tracking_file = f"tracking_{current_time}.log"
        tracking_data = f"Build detected:\nHostname: {hostname}\nTimestamp: {current_time}\n\n"

        # Step 2: Write tracking data to a timestamped log file
        with open(tracking_file, "w") as file:
            file.write(tracking_data)

        # Step 3: Push the tracking log to the public GitHub repository
        repo_url = "https://github.com/rakesh9177/Tracking.git"
        local_repo_path = "/tmp/tracking-repo"

        # Clone the tracking repository to a temporary directory
        if os.path.exists(local_repo_path):
            subprocess.check_call(["rm", "-rf", local_repo_path])  # Clean up if already exists
        subprocess.check_call(["git", "clone", repo_url, local_repo_path])

        # Copy the tracking file into the cloned repository
        subprocess.check_call(["cp", tracking_file, os.path.join(local_repo_path, tracking_file)])

        # Navigate to the cloned repository
        os.chdir(local_repo_path)

        # Add, commit, and push the tracking file
        subprocess.check_call(["git", "add", tracking_file])
        subprocess.check_call(["git", "commit", "-m", f"Add {tracking_file}"])
        subprocess.check_call(["git", "push", "origin", "main"])

        print(f"Tracking file {tracking_file} pushed to the repository.")

        # Step 4: Clean up the cloned repository and local log file
        os.chdir("/")  # Move out of the directory before deleting
        subprocess.check_call(["rm", "-rf", local_repo_path])
        os.remove(tracking_file)
        print("Cleaned up tracking resources.")
    except Exception as e:
        print(f"Error during tracking: {e}")

if __name__ == "__main__":
    track_and_push()
