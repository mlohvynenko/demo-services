#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from enum import Enum
from .base_converter import BaseGeniviConverter


class TurnLight(Enum):
    LEFT = "left"
    RIGHT = "right"
    STRAIGHT = "straight"


class TurnLightGeniviConverter(BaseGeniviConverter):
    NONE_DEFAULT_VALUE = False

    def __init__(self, *args, side: TurnLight, **kwargs):
        super().__init__(*args, **kwargs)
        self._side = side

    def _convert_value(self, instance, value):
        try:
            return self._side == TurnLight(value)
        except ValueError:
            print("Not valid turn light data: '{}'".format(value))
            return False


class TurnLightLeverGeniviConverter(BaseGeniviConverter):
    NONE_DEFAULT_VALUE = 0

    def __init__(self, hazard_src, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hazard_src = hazard_src

    def _convert_value(self, instance, value):
        result = 0
        try:
            side = TurnLight(value)
            if not instance.data.get(self._hazard_src) and side != TurnLight.STRAIGHT:
                result = 1 if side == TurnLight.LEFT else 2
        except ValueError:
            print("Not valid turn light data: '{}'".format(value))
        return result
