import logging
from copy import deepcopy

import numpy as np

from .component import Component

class Delay(Component):
    def __init__(self, sample_rate, frames_per_chunk, subcomponents, name="Delay", control_tag="delay") -> None:
        super().__init__(sample_rate, frames_per_chunk, subcomponents=subcomponents, name=name, control_tag=control_tag)
        self.log = logging.getLogger(__name__)
        self.delay_buffer_length = 4.0
        self._delay_time = 0.0
        self.delay_frames = int(self.delay_buffer_length * self.sample_rate)
        self.delay_buffer = np.zeros(self.delay_frames, np.float32)
        self.delay_time_start_index = self.delay_frames - int(self.delay_time * self.sample_rate)
        self.wet_gain = 0.5 

    def __iter__(self):
        self.signal_iter = iter(self.subcomponents[0])
        return self
    
    def __next__(self):
        mix = next(self.signal_iter)
        
        # Add the delayed signal to the mix
        if self.delay_time > 0:
            delayed_signal = self.delay_buffer[self.delay_time_start_index: self.delay_time_start_index + self.frames_per_chunk]
            while len(delayed_signal) < self.frames_per_chunk:
                delayed_signal = np.concatenate((delayed_signal, self.delay_buffer[:self.frames_per_chunk - len(delayed_signal)]))
            
            delayed_signal *= self.wet_gain
            mix += delayed_signal

        # Add the current signal to the delay buffer
        self.delay_buffer = np.roll(self.delay_buffer, -self.frames_per_chunk)
        self.delay_buffer[self.delay_frames - self.frames_per_chunk: self.delay_frames] = mix

        return mix

    
    def __deepcopy__(self, memo):
        return Delay(self.sample_rate, self.frames_per_chunk, subcomponents=[deepcopy(sub, memo) for sub in self.subcomponents], name=self.name, control_tag=self.control_tag)
    
    @property
    def delay_time(self):
        return self._delay_time

    @delay_time.setter
    def delay_time(self, value):
        self._delay_time = float(value)
        self.delay_time_start_index = self.delay_frames - int(self.delay_time * self.sample_rate)
