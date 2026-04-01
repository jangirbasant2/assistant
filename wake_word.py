import pvporcupine
import pyaudio
import struct


def listen_wake(callback):

    porcupine = pvporcupine.create(keywords=["jarvis"])

    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    while True:

        pcm = stream.read(porcupine.frame_length)

        pcm = struct.unpack_from("h"*porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:

            callback()