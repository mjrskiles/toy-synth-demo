import logging
import numpy as np

from .generator import Generator

class Oscillator(Generator):
    """
    The base class for any component that generates a signal with frequency.
    """
    def __init__(self, sample_rate: int, frames_per_chunk: int, name: str="Oscillator"):
        super().__init__(sample_rate, frames_per_chunk, name=name)
        self.log = logging.getLogger(__name__)
        self.frequency = 0.0
        self.phase = 0.0
        self.amplitude = 0.1

    @property
    def frequency(self):
        """The wave frequency in hertz"""
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        try:
            float_value = float(value)
            self._frequency = float_value
        except:
            self.log.error(f"unable to set with value {value}")

    @property
    def phase(self):
        """The phase offset of the wave in radians"""
        return self._phase
    
    @phase.setter
    def phase(self, value):
        try:
            float_value = float(value)
            self._phase = float_value
        except:
            self.log.error(f"unable to set with value {value}")

    def set_phase_degrees(self, degrees):
        """
        Convenience method to set the phase offset in degrees instead of radians
        """
        try:
            radians = (degrees / 360) * 2 * np.pi
            self.phase = radians
        except:
            self.log.error(f"unable to set with value {degrees}")

    @property
    def amplitude(self):
        """The wave amplitude from 0.0 to 1.0"""
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        try:
            float_value = float(value)
            if float_value >= 0.0 and float_value <= 1.0:
                self._amplitude = float_value
            else:
                raise ValueError
        except:
            self.log.error(f"unable to set with value {value}")

    @property
    def active(self):
        """
        Whether or not the oscillator is active
        Overrides the active property of the Component class
        """
        return self._active
    
    @active.setter
    def active(self, value):
        try:
            bool_val = bool(value)
            self._active = bool_val
            self.frequency = 0.0 if not bool_val else self.frequency
        except ValueError:
            self.log.error(f"Unable to set with value {value}")