import logging
import threading
import queue

import mido

from . import message_builder as mb

class MidiListener(threading.Thread):
    """
    Listens for MIDI messages on a given port and sends them to the synth mailbox.
    """
    def __init__(self, thread_mailbox: queue.Queue, synth_mailbox: queue.Queue, port_name: str):
        super().__init__(name=f"{port_name}-listener")
        self.log = logging.getLogger(__name__)
        self.thread_mailbox = thread_mailbox # The mailbox that receives commands from the main thread. Namely the 'exit' command to shut down gracefully.
        self.synth_mailbox = synth_mailbox # The OUT mailbox where we send the parsed commands to be played by the synth
        self.port_name = port_name
    
    def run(self):
        should_run = True
        inport = None

        try:
            inport = mido.open_input(self.port_name)
            self.log.info(f"Opened port {self.port_name}")
        except:
            self.log.error(f"Failed to open MIDI port at {self.port_name}. Closing the listener thread.")
            should_run = False

        while should_run:
            # Receive MIDI messages from the port and send them to the synth mailbox
            if msg := inport.receive():
                match msg.type:
                    case "note_on":
                        ctrl_msg = mb.builder().note_on().with_note(msg.note).on_channel(msg.channel).build()
                        self.synth_mailbox.put(ctrl_msg)
                    case "note_off":
                        ctrl_msg = mb.builder().note_off().with_note(msg.note).on_channel(msg.channel).build()
                        self.synth_mailbox.put(ctrl_msg)
                    case "control_change":
                        ctrl_msg = mb.builder().control_change().on_channel(msg.channel).with_control_num(msg.control).with_value(msg.value).build()
                        self.synth_mailbox.put(ctrl_msg)
                    case "stop":
                        self.log.info(f"Received midi STOP message")
                    case _:
                        self.log.info(f"Matched unknown MIDI message: {msg}")
            
            # get_nowait raises queue.Empty exception if there is nothing in the queue
            # We don't want to block this thread checking for thread command messages
            try:
                if mail := self.thread_mailbox.get_nowait():
                    match mail.split():
                        case ['exit']:
                            self.log.info("Got exit command.")
                            should_run = False
                        case _:
                            self.log.info(f"Matched unknown mailbox message: {mail}")
            except queue.Empty:
                pass

        if inport is not None:
            inport.close()
        return