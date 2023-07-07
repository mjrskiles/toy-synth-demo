from .signal.chain import Chain

class Voice:
    def __init__(self, signal_chain: Chain):
        self.signal_chain = iter(signal_chain)
        self.note_id = None

    @property
    def active(self):
        return self.signal_chain.active

    def note_on(self, frequency, id):
        self._active = True
        self.note_id = id
        self.signal_chain.note_on(frequency)

    def note_off(self):
        self.signal_chain.note_off()