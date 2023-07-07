import logging
import queue
import sys
from optparse import OptionParser
from time import sleep

import synth.midi as midi
from . import settings
from .playback.stream_player import StreamPlayer
from .synthesis.signal.sine_wave_oscillator import SineWaveOscillator
from .synthesis.signal.square_wave_oscillator import SquareWaveOscillator
from .synthesis.signal.gain import Gain
from .synthesis.signal.mixer import Mixer
from .midi.midi_listener import MidiListener

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="midi_port", default=None, help="MIDI port to listen on", metavar="MIDI_PORT")
    (options, args) = parser.parse_args()

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

    # Create a stream player
    stream_player = StreamPlayer(sample_rate=settings.sample_rate, frames_per_chunk=settings.frames_per_chunk, input_delegate=mixer)

    listener_mailbox = queue.Queue()
    synth_mailbox = queue.Queue()

    midi_listen_port = options.midi_port if options.midi_port else settings.auto_attach
    log.info(f"Using MIDI port {midi_listen_port}")
    midi_listener = MidiListener(listener_mailbox, synth_mailbox, midi_listen_port)
    
    try:
        stream_player.play()
        midi_listener.start()
        current_note = None
        while True:
            if synth_mail := synth_mailbox.get():
                log.info(f"{synth_mail}")
                match synth_mail.split():
                    case ["note_on", "-n", note, "-c", channel]:
                        int_note = int(note)
                        freq = midi.frequencies[int_note]
                        osc_a.frequency = float(freq)
                        osc_b.frequency = float(freq)
                        current_note = note
                    case ["note_off", "-n", note, "-c", channel]:
                        if current_note == note:
                            osc_a.frequency = 0.0
                            osc_b.frequency = 0.0
                            current_note = None
    except KeyboardInterrupt:
        log.info("Caught keyboard interrupt. Exiting the program.")

    stream_player.stop()
    listener_mailbox.put("exit")
    midi_listener.join()
    sys.exit(0)