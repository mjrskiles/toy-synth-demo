import logging
from typing import List
import random

class Component():
    """
    Represents a base signal component. A signal component is an iterator.
    The iterator should return an ndarray of size <frames_per_chunk> with type numpy.float32
    where props is a dictionary of properties related to the array.

    A component can have a list of subcomponents, which should also be iterators.

    A component must implement
    __iter__
    __next__
    __deepcopy__
    """

    def __init__(self, sample_rate: int, frames_per_chunk: int, subcomponents: List['Component']=[], name="Component", control_tag: str = ""):
        self.log = logging.getLogger(__name__)
        self.sample_rate = sample_rate
        self.frames_per_chunk = frames_per_chunk
        self.subcomponents = subcomponents
        self.active = False
        self.name = name + "#" + str(random.randint(0, 9999))
        self.control_tag = control_tag

    def __iter__(self):
        return self
    
    def __next__(self):
        self.log.error("Child class should override the __next__ method")
        raise NotImplementedError
    
    def __deepcopy__(self, memo):
        self.log.error("invoked deepcopy on base class")
        raise NotImplementedError
    
    @property
    def sample_rate(self):
        """The number of sample slices per second"""
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        try:
            int_value = int(value)
            self._sample_rate = int_value
        except ValueError:
            self.log.error(f"unable to set with value {value}")

    @property
    def frames_per_chunk(self):
        """The number of data frames to generate per call to __next__. Essentially the size of the array to generate"""
        return self._frames_per_chunk
    
    @frames_per_chunk.setter
    def frames_per_chunk(self, value):
        try:
            int_value = int(value)
            self._frames_per_chunk = int_value
        except ValueError:
            self.log.error(f"unable to set with value {value}")

    @property
    def active(self):
        """
        The active status.
        When a component is active it should perform its function
        When it is inactive it should either return zeros or bypass the signal.
        If the component is a generator it should generate zeros when inactive.
        """
        return self._active
    
    @active.setter
    def active(self, value):
        try:
            bool_val = bool(value)
            self._active = bool_val
            for sub in self.subcomponents:
                sub.active = bool_val
        except ValueError:
            self.log.error(f"Unable to set with value {value}")
    
    def get_subcomponents_str(self, component, depth):
        """
        Returns an indented string representing the tree of subcomponents
        """
        ret_str = ""
        for _ in range(depth):
            ret_str += "  "
        ret_str += f"{component.name}\n"    
        if hasattr(component, "subcomponents") and len(component.subcomponents) > 0:
            for subcomponent in component.subcomponents:
                ret_str += self.get_subcomponents_str(subcomponent, depth + 1)
        return ret_str
    
    def __str__(self):
        ret_str = self.get_subcomponents_str(self, 0)
        return ret_str
