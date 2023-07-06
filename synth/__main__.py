import logging
from time import sleep

import numpy as np

from . import settings
from .playback.stream_player import StreamPlayer

def sine_generator(frequency, amplitude, sample_rate, frames_per_chunk):
    """
    A generator which yields a sine wave of frequency <frequency> and amplitude <amplitude>.
    """
    chunk_duration = frames_per_chunk / sample_rate
    chunk_start_time = 0.0
    chunk_end_time = chunk_duration
    phase = 0.0
    while True:
        # Generate the wave
        if frequency <= 0.0:
            if frequency < 0.0:
                log.error("Overriding negative frequency to 0")
            amplitude = 0.0
            wave = np.zeros(frames_per_chunk)
        
        else:
            wave = amplitude * np.sin(phase + (2 * np.pi * frequency) * np.linspace(chunk_start_time, chunk_end_time, frames_per_chunk, endpoint=False))

        # Update the state variables for next time
        chunk_start_time = chunk_end_time
        chunk_end_time += chunk_duration

        yield wave.astype(np.float32)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s [%(levelname)s] %(module)s [%(funcName)s]: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    log = logging.getLogger(__name__)
    log.info(
        """
    __
   |  |
 __|  |___             ______         __        __
/__    __/          __|______|__     |  |      |  |
   |  |            |  |      |  |    |__|______|  |
   |  |     __     |  |      |  |       |______   |
   |__|____|__|    |__|______|__|        ______|__|
      |____|          |______|          |______|

                                                            __              __
                                                           |  |            |  |
    _______         __        __      __    ____         __|  |___         |  |   ____
 __|_______|       |  |      |  |    |  |__|____|__     /__    __/         |  |__|____|__
|__|_______        |__|______|  |    |   __|    |  |       |  |            |   __|    |  |
   |_______|__        |______   |    |  |       |  |       |  |     __     |  |       |  |
 __________|__|        ______|__|    |  |       |  |       |__|____|__|    |  |       |  |
|__________|          |______|       |__|       |__|          |____|       |__|       |__|
        """
    )

    # Create a sine wave generator
    sine_wave_generator = sine_generator(frequency=440.0, amplitude=0.5, sample_rate=settings.sample_rate, frames_per_chunk=settings.frames_per_chunk)

    # Create a stream player
    stream_player = StreamPlayer(sample_rate=settings.sample_rate, frames_per_chunk=settings.frames_per_chunk, input_delegate=sine_wave_generator)
    stream_player.play()
    while True:
        sleep(1)