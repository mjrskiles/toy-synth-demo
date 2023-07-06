from copy import deepcopy
from typing import List

import numpy as np

from .component import Component

class Mixer(Component):
    def __init__(self, sample_rate: int, frames_per_chunk: int, subcomponents: List[Component] = [], name: str="Mixer"):
        super().__init__(sample_rate, frames_per_chunk, subcomponents, name)

    def __iter__(self):
        self.source_iters = [iter(component) for component in self.subcomponents]
        return self

    def __next__(self):
        input_signals = [next(source_iter) for source_iter in self.source_iters]
        mixed_signal = np.mean(input_signals, axis=0)
        mixed_signal = np.clip(mixed_signal, -1.0, 1.0)
        return mixed_signal.astype(np.float32)

    def __deepcopy__(self, memo):
        return Mixer(self.sample_rate, self.frames_per_chunk, [deepcopy(component, memo) for component in self.subcomponents], self.name)
