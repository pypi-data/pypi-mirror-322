import pyaudio
import json

def start_audio_stream(client_socket):
    p = pyaudio.PyAudio()

    input_device_count = p.get_device_count()
    input_device_found = False
    for i in range(input_device_count):
        if p.get_device_info_by_index(i).get('maxInputChannels') > 0:
            input_device_found = True
            break

    if not input_device_found:
        client_socket.sendall(json.dumps({"logger": "No input device found"}).encode())
        return

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    while True:
        try:
            audio_data = stream.read(1024)
            client_socket.sendall(audio_data)
        except (ConnectionError, ConnectionResetError):
            pass
        except Exception as e:
            message = f"From Remote: {str(e)}"
            client_socket.sendall(json.dumps({"logger": message}).encode())