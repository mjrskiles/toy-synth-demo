import logging
from copy import deepcopy

import numpy as np

from .generator import Generator

class NoiseGenerator(Generator):
    def __init__(self, sample_rate, frames_per_chunk, name="Noise Generator"):
        super().__init__(sample_rate, frames_per_chunk, name=name)
        self.log = logging.getLogger(__name__)
        self.amp = 0.1

    def __iter__(self):
        self.rng = np.random.default_rng()
        return super().__iter__()
    
    def __next__(self):
        if self.active:
            noise = self.amp * self.rng.uniform(-1.0, 1.0, self.frames_per_chunk)
            return noise.astype(np.float32)
        else:
            return np.zeros(self.frames_per_chunk, dtype=np.float32)
    
    def __deepcopy__(self, memo):
        return NoiseGenerator(self.sample_rate, self.frames_per_chunk)