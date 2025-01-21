import subprocess
import threading
import queue

def create_shell():
    def read_output(pipe, output_queue):
        for line in iter(pipe.readline, ''):
            output_queue.put(line)
        pipe.close()

    shell = subprocess.Popen(
        ["cmd.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    stdout_queue = queue.Queue()
    stderr_queue = queue.Queue()

    stdout_thread = threading.Thread(target=read_output, args=(shell.stdout, stdout_queue))
    stderr_thread = threading.Thread(target=read_output, args=(shell.stderr, stderr_queue))
    stdout_thread.daemon = True
    stderr_thread.daemon = True
    stdout_thread.start()
    stderr_thread.start()

    return shell, stdout_queue, stderr_queue
