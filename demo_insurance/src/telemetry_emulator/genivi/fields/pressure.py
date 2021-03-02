#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from .base_converter import BaseGeniviConverter


class PressureKPAToPSIConverter(BaseGeniviConverter):
    NONE_DEFAULT_VALUE = 255

    def _convert_value(self, instance, value):
        return value // 6.895
