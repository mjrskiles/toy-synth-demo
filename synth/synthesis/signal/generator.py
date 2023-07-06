import logging

from .component import Component

class Generator(Component):
    def __init__(self, sample_rate: int, frames_per_chunk: int, name: str="Generator"):
        """
        The base class for any signal component that can generate signal.
        Generators should be leaf nodes on the signal tree. That means they have no subcomponents.
        """
        super().__init__(sample_rate, frames_per_chunk, [], name=name)
        self.log = logging.getLogger(__name__)