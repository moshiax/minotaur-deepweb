import subprocess

for _ in range(20):
    subprocess.Popen(["python", "searchbyname.py"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW, close_fds=True)
