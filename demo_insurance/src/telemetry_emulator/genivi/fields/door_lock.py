#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from .base_converter import BaseGeniviConverter


class DoorLockConverter(BaseGeniviConverter):
    NONE_DEFAULT_VALUE = 3

    def __init__(self, fl, fr, rl, rr):
        super().__init__(src_name=None)
        self._front_left_door = fl
        self._front_right_door = fr
        self._rear_left_door = rl
        self._rear_right_door = rr

    def _get_value(self, instance):
        fl = instance.data.get(self._front_left_door)
        fr = instance.data.get(self._front_right_door)
        rl = instance.data.get(self._rear_left_door)
        rr = instance.data.get(self._rear_right_door)

        overall_status = (fl, fr, rl, rr,)
        result = self.NONE_DEFAULT_VALUE
        if None not in overall_status:
            if all(overall_status):
                result = 0
            elif not any(overall_status):
                result = 2
            elif not fl:
                result = 1

        return result
