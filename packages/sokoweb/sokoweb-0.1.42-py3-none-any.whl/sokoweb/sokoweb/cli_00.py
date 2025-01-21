# File: cli.py
import os
import subprocess
import sys
import shutil
import tempfile
import re
from pathlib import Path
from importlib import resources  # Python 3.9+

def read_existing_env(env_path):
    existing_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    existing_vars[key.strip()] = value.strip()
    return existing_vars

def validate_port(port):
    try:
        port = int(port)
        return 1024 <= port <= 65535
    except ValueError:
        return False

def validate_hostname(hostname):
    if not hostname:
        return False
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}|[a-zA-Z0-9\.-]+$')
    return bool(ip_pattern.match(hostname))

def prompt_for_three_vars(existing_vars):
    """Prompt ONLY for NODE_PORT, NODE_TCP_PORT, ADVERTISE_IP.
    If user hits Enter, keep existing .env value or use defaults."""

    # 1) NODE_PORT
    default_node_port = existing_vars.get('NODE_PORT', '8000')
    while True:
        node_port = input(
            f"Enter NODE_PORT (press Enter for default {default_node_port}): "
        ).strip()
        if not node_port:
            node_port = default_node_port
        if validate_port(node_port):
            existing_vars["NODE_PORT"] = node_port
            break
        print("Invalid port! Must be between 1024 and 65535.")

    # 2) NODE_TCP_PORT
    default_tcp_port = existing_vars.get('NODE_TCP_PORT', '8500')
    while True:
        node_tcp_port = input(
            f"Enter NODE_TCP_PORT (press Enter for default {default_tcp_port}): "
        ).strip()
        if not node_tcp_port:
            node_tcp_port = default_tcp_port
        if validate_port(node_tcp_port):
            existing_vars["NODE_TCP_PORT"] = node_tcp_port
            break
        print("Invalid port! Must be between 1024 and 65535.")

    # 3) ADVERTISE_IP
    default_ip = existing_vars.get('ADVERTISE_IP', 'localhost')
    while True:
        advertise_ip = input(
            f"Enter ADVERTISE_IP (e.g., example.com) [default {default_ip}]: "
        ).strip()
        if not advertise_ip:
            advertise_ip = default_ip
        if validate_hostname(advertise_ip):
            existing_vars["ADVERTISE_IP"] = advertise_ip
            break
        print("Invalid hostname/IP! Please enter a valid hostname or IP address.")

def write_env(env_path, vars_dict):
    try:
        with open(env_path, 'w') as f:
            for k, v in vars_dict.items():
                f.write(f"{k}={v}\n")
    except Exception as e:
        print(f"Error writing .env: {e}")
        sys.exit(1)

SOKOWEB_TEMPFILE_NAME = ".sokoweb_temp_dir"

def up(detached=False):
    """
    Bring up Docker containers using a temporary directory for docker-compose.yml.
    Store the temp directory path locally so we can reference it later in 'down()'.
    """
    print("\nSetting up environment variables...")

    # 1) Create a persistent temp directory (mkdtemp instead of TemporaryDirectory)
    temp_dir_path = tempfile.mkdtemp()

    # 2) Copy Dockerfile + docker-compose.yml into that temp directory
    docker_dir = resources.files("sokoweb.docker")
    shutil.copyfile(docker_dir / "Dockerfile", f"{temp_dir_path}/Dockerfile")
    shutil.copyfile(docker_dir / "docker-compose.yml", f"{temp_dir_path}/docker-compose.yml")

    # 3) Prepare .env in the temp directory (pull from user’s local .env if it exists)
    env_path = Path(temp_dir_path) / ".env"
    user_env = Path.cwd() / ".env"
    if user_env.exists():
        shutil.copyfile(user_env, env_path)

    # 4) Load or prompt for variables as needed
    existing_vars = read_existing_env(env_path)
    prompt_for_three_vars(existing_vars)

    # If ADVERTISE_IP == 'localhost', set BOOTSTRAP_NODES to an empty string
    if existing_vars.get("ADVERTISE_IP", "") == "localhost":
        existing_vars["BOOTSTRAP_NODES"] = ""

    # 5) Write the final .env back
    write_env(env_path, existing_vars)

    print("\nUpdated environment variables (from .env in the temp directory):")
    for k, v in existing_vars.items():
        print(f"{k}={v}")

    # 6) Save the temp directory path to a small file in the current directory
    with open(SOKOWEB_TEMPFILE_NAME, "w") as f:
        f.write(temp_dir_path)

    # 7) Start Docker
    print("\nStarting Docker containers...")
    compose_cmd = ["docker", "compose", "-f", "docker-compose.yml", "up", "--build"]
    if detached:
        compose_cmd.append("-d")

    try:
        process = subprocess.run(
            compose_cmd,
            check=True,
            cwd=temp_dir_path
        )
        if process.returncode == 0:
            if detached:
                print("Successfully started Docker containers in detached mode.")
            else:
                print("Successfully started Docker containers.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker containers (exit code={e.returncode})")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

def down():
    """
    Stop/remove containers (and volumes) by reading the temp_dir path from .sokoweb_temp_dir.
    """
    print("Stopping Docker containers and removing volumes...")

    # 1) Check if the .sokoweb_temp_dir file exists
    temp_file = Path.cwd() / SOKOWEB_TEMPFILE_NAME
    if not temp_file.exists():
        print(f"No {SOKOWEB_TEMPFILE_NAME} file found in the current directory.")
        print("Cannot determine where docker-compose.yml is located.")
        return

    # 2) Read the path
    with open(temp_file, "r") as f:
        temp_dir_path = f.read().strip()

    # 3) If the docker-compose.yml in that path doesn’t exist, warn and return
    docker_compose_file = Path(temp_dir_path) / "docker-compose.yml"
    if not docker_compose_file.exists():
        print("No docker-compose.yml found in the stored temp directory path!")
        return

    # 4) Run "docker compose down" from that path
    try:
        subprocess.run(
            ["docker", "compose", "-f", str(docker_compose_file), "down", "-v"],
            check=True,
            cwd=temp_dir_path
        )
        print("Successfully stopped and removed containers/volumes.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Docker containers (exit code={e.returncode})")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    # 5) (Optional) Remove the temp directory we created, if desired:
    # import shutil
    # shutil.rmtree(temp_dir_path, ignore_errors=True)
    # temp_file.unlink(missing_ok=True)  # remove the .sokoweb_temp_dir file too

if __name__ == "__main__":
    """
    If someone calls python cli.py [options], we parse arguments quickly:
    -d or --detached => run up() in detached mode
    down => run down()
    Otherwise => run up() in foreground mode
    """
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "down":
            down()
        elif arg in ["-d", "--detached"]:
            up(detached=True)
        else:
            up(detached=False)
    else:
        up(detached=False)