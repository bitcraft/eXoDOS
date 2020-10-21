import subprocess

try:
    subprocess.run("huey_consumer pyxodos.main.huey -k process -w 4", shell=True)
except KeyboardInterrupt:
    print("\naborting...")
