from yta_general_utils.programming.enum import YTAEnum as Enum
from abc import ABC, abstractmethod
from typing import Tuple, Union

import numpy as np


# TODO: Move this class to its own file
class SEffectType(Enum):
    """
    Type of SEffects that we are able to handle, useful to
    recognize if we are trying to apply two (or more) 
    effects of the same type and use only one of them.

    TODO: I don't know how to indicate the type correctly
    so I can decide I'm only able to use one of that type.
    """
    GENERAL = 'general'
    """
    I don't know which type is this effect and I'm not
    blocking it.
    """
    MOVEMENT = 'movement'
    """
    Effect hat only affects to 'with_position' array.
    """

# TODO: What about the effects that modifies the
# image frame values? Should I use 
class SEffect(ABC):
    """
    Class to apply and effect and return its 'with_position',
    'rotated' and 'resized' parameters.

    This class must be implemented by any specific and 
    custom effect that applies to a SubClip instance.
    """
    def __init__(self, number_of_frames: int, type: SEffectType, *args, **kwargs):
        type = SEffectType.to_enum(type)

        self.number_of_frames = number_of_frames
        self.type = type
        self.args = args
        self.kwargs = kwargs

    @property
    @abstractmethod
    def do_affect_frames(self) -> bool:
        """
        Return True if the effect affects to the 'frames'
        array or not.
        """
        return self.calculate(1)[0] is None

    @property
    @abstractmethod
    def do_affect_with_position(self) -> bool:
        """
        Return True if the effect affects to the 'with_position'
        array or not.
        """
        return self.calculate(1)[1] is None

    @property
    @abstractmethod
    def do_affect_resized(self) -> bool:
        """
        Return True if the effect affects to the 'resized'
        array or not.
        """
        return self.calculate(1)[2] is None

    @property
    @abstractmethod
    def do_affect_rotated(self) -> bool:
        """
        Return True if the effect affects to the 'rotated'
        array or not.
        """
        return self.calculate(1)[3] is None

    @property
    @abstractmethod
    def values(self) -> Tuple[Union[list[np.ndarray], None], Union[list[int, int], None], Union[list[float, float], None], Union[int, None]]:
        """
        Calculate the values for the 4 arrays 'frames',
        'with_position', 'resized', and 'rotated' and return
        each of them if affected, or None if not.
        """
        return self.calculate(self.number_of_frames, *self.args, **self.kwargs)
    
    @staticmethod
    @abstractmethod
    def calculate(number_of_frames: int, *args, **kwargs) -> Tuple[Union[list[np.ndarray], None], Union[list[int, int], None], Union[list[float, float], None], Union[int, None]]:
        """
        Calculate the values for the 4 arrays 'frames',
        'with_position', 'resized', and 'rotated' with
        the provided 'number_of_frames' and additional
        arguments and return each of them if affected,
        or None if not.
        """
        return None, None, None, None