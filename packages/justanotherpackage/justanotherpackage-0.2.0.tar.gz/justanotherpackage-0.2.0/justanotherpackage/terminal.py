import time

def terminal(data, client_socket, shell, stdout_queue, stderr_queue):
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

    client_socket.sendall(output.encode('utf-8') if output else b"Command executed successfully.\n")
