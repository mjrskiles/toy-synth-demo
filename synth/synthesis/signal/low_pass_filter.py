import logging
from typing import List
from copy import deepcopy

import numpy as np
from scipy.signal import butter, lfilter, lfilter_zi

from .component import Component

class LowPassFilter(Component):
    def __init__(self, sample_rate: int, frames_per_chunk: int, subcomponents: List['Component'] = [], name: str="LowPassFilter", control_tag: str="lpf"):
        super().__init__(sample_rate, frames_per_chunk, subcomponents=subcomponents, name=name, control_tag=control_tag)
        self.log = logging.getLogger(__name__)
        self.filter_order = 2
        self.cutoff_frequency = 20000.0
        self.b, self.a = self.compute_coefficients()
        self.zi = self.compute_initial_conditions()

    def __iter__(self):
        self.source_iter = iter(self.subcomponents[0])
        return self

    def __next__(self):
        input_signal = next(self.source_iter)
        output_signal, self.zi = lfilter(self.b, self.a, input_signal, zi=self.zi)
        return output_signal.astype(np.float32)

    def __deepcopy__(self, memo):
        return LowPassFilter(self.sample_rate, self.frames_per_chunk, [deepcopy(self.subcomponents[0], memo)], name=self.name, control_tag=self.control_tag)

    @property
    def cutoff_frequency(self):
        return self._cutoff_frequency
    
    @cutoff_frequency.setter
    def cutoff_frequency(self, value):
        try:
            float_val = float(value)
            if float_val < 0.0:
                raise ValueError("Cutoff frequency must be positive.")
            self._cutoff_frequency = float_val
            self.b, self.a = self.compute_coefficients()
        except ValueError:
            self.log.error(f"Couldn't set with value {value}")

    def compute_coefficients(self):
        nyquist = 0.5 * self.sample_rate
        normalized_cutoff = self.cutoff_frequency / nyquist
        b, a = butter(self.filter_order, normalized_cutoff, btype='low', analog=False)
        return b, a

    def compute_initial_conditions(self):
        zi = lfilter_zi(self.b, self.a)
        return zi
