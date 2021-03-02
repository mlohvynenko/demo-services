#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from .base_converter import BaseGeniviConverter


class SpeedGeniviConverter(BaseGeniviConverter):

    def _convert_value(self, instance, value):
        return value // 1000  # mph to kmph
