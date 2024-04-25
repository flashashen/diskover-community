import os
import subprocess
import requests
import argparse

REPO_ASSETS = 'flashashen/diskover-community'

ENV_FILE_CONTENTS = '''
# The root directory on the host to scan
DISKOVER_SCAN_DIR={DISKOVER_SCAN_DIR}\n

DISKOVER_IMAGE_VERSION={DISKOVER_IMAGE_VERSION}\n

# No admin UI in Community Edition
DISKOVER_ADMIN_PORT=
'''


def download_asset(repo, asset_path):

    filename = asset_path.split('/')[-1]
    if os.path.exists(filename):
        print(f'{filename} already exists')
        return

    print(f'downloading {filename}...')
    url = f'https://raw.githubusercontent.com/{repo}{asset_path}'
    r = requests.get(url)
    if not r:
        print(f'Failed to fetch {url}: {r}')
        exit(1)

    with open(filename, 'wb') as fd:
        fd.write(r.content)
  

def prompt_scan_dir():
    scan_dir = input("Enter host directory to scan: ")
    scan_dir = os.path.abspath(os.path.expanduser(scan_dir))
    if not os.path.exists(os.path.abspath(scan_dir)):
        print(f'{scan_dir} does not exist')
        exit(1)
    return scan_dir


def get_compose_env(host_scan_dir):
     return {
        'DISKOVER_SCAN_DIR': host_scan_dir if host_scan_dir else '.',
        'DISKOVER_IMAGE_VERSION': '2.3.0_build_20240424'
    } | os.environ.copy()   # give precedence to system env


def write_compose_env(host_scan_dir):

    if os.path.exists('.env'):
        print(f'.env already exists')
        return {}

    with open('.env', 'w') as fd:
        print(f'writing docker compose .env file')
        fd.write(ENV_FILE_CONTENTS.format(**get_compose_env(host_scan_dir)))


def compose_up():
    print('starting diskover with docker compose in daemon mode')
    subprocess.call(
        ['docker', 'compose', 'up', '-d'])



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sd",
          "--host_scan_dir", 
          help='The directory on the host to mount in the container for scans. If the .env file has already beeen written this option will have no effect.')
    args = parser.parse_args()

    download_asset(REPO_ASSETS, '/docker/docker/start.py')
    download_asset(REPO_ASSETS, '/docker/docker/docker-compose.yml')
    write_compose_env(args.host_scan_dir)
    compose_up()