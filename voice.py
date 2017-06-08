from __future__ import print_function

import pyaudio
import wave
import numpy as np
import time
import io
import threading
import requests

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 8096

VOICE_SERVER = 'http://toosyou.nctu.me:8888'

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
    stream.start_stream()

    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=True)
            stream.write(data, CHUNK)
        except:
            print('failed to read')
            data = np.zeros(CHUNK, dtype=np.int16).tostring()
            time.sleep(0.5)

        header = {'time':str(time.time())}
        try:
            requests.post(VOICE_SERVER, data=str(data), headers=header)
            print('sent!')
        except:
            print('unsent!')

    stream.stop_stream()
    stream.close()
    p.terminate()
