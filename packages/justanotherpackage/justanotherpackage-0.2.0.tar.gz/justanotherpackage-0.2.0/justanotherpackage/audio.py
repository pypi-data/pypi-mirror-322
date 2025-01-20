import pyaudio

def start_audio_stream(client_socket):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    while True:
        try:
            audio_data = stream.read(1024)
            client_socket.sendall(audio_data)
        except Exception as e:
            break