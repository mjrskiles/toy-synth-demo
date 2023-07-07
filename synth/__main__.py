import logging
import queue
import sys
from optparse import OptionParser
from time import sleep

from . import settings
from .midi.midi_listener import MidiListener
from .synthesizer import Synthesizer

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

    listener_mailbox = queue.Queue()
    synth_mailbox = queue.Queue()

    midi_listen_port = options.midi_port if options.midi_port else settings.auto_attach
    log.info(f"Using MIDI port {midi_listen_port}")
    midi_listener = MidiListener(listener_mailbox, synth_mailbox, midi_listen_port)

    synthesizer = Synthesizer(settings.sample_rate, settings.frames_per_chunk, synth_mailbox)
    
    try:
        midi_listener.start()
        synthesizer.start()
        while True:
            sleep(1)
    except KeyboardInterrupt:
        log.info("Caught keyboard interrupt. Exiting the program.")

    listener_mailbox.put("exit")
    synth_mailbox.put("exit")
    synthesizer.join()
    midi_listener.join()
    sys.exit(0)