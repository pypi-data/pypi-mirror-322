from yta_multimedia.video.edition.s_effect.s_effect import SEffect, SEffectType
from typing import Tuple, Union

import numpy as np


class ExampleEffect(SEffect):
    def __init__(
        self,
        number_of_frames: int,
        value: int
    ):
        super().__init__(number_of_frames, SEffectType.GENERAL)

        self.value = value

    @staticmethod
    def calculate(number_of_frames: int, value) -> Tuple[Union[list[np.ndarray], None], Union[list[int, int], None], Union[list[float, float], None], Union[int, None]]:
        """
        Calculate the values for the 3 arrays 'with_position',
        'resized', and 'rotated' and return each of them if
        affected, or None if not.
        """
        return None, None, [value * 0.1 for _ in range(number_of_frames)], None