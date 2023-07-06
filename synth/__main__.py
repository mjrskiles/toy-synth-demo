import logging
from time import sleep

from . import settings
from .playback.stream_player import StreamPlayer
from .synthesis.signal.sine_wave_oscillator import SineWaveOscillator
from .synthesis.signal.square_wave_oscillator import SquareWaveOscillator
from .synthesis.signal.gain import Gain
from .synthesis.signal.mixer import Mixer

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

    # create a sine wave oscillator
    osc_a = SineWaveOscillator(settings.sample_rate, settings.frames_per_chunk)
    osc_b = SquareWaveOscillator(settings.sample_rate, settings.frames_per_chunk)

    gain_a = Gain(settings.sample_rate, settings.frames_per_chunk, subcomponents=[osc_a])
    gain_b = Gain(settings.sample_rate, settings.frames_per_chunk, subcomponents=[osc_b])

    mixer = Mixer(settings.sample_rate, settings.frames_per_chunk, subcomponents=[gain_a, gain_b])

    osc_a.frequency = 440.0
    osc_b.frequency = 440.0

    # Create a stream player
    stream_player = StreamPlayer(sample_rate=settings.sample_rate, frames_per_chunk=settings.frames_per_chunk, input_delegate=mixer)
    
    try:
        stream_player.play()
        while True:
            sleep(1)
    except KeyboardInterrupt:
        log.info("Caught keyboard interrupt. Exiting the program.")