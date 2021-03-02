#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from .exceptions import GeniviConverterCanNotClarifyNameException


class BaseGeniviConverter:
    NONE_DEFAULT_VALUE = None

    def __init__(self, src_name):
        self._src_name = src_name

    def _get_name(self, owner):
        for name, obj in owner.__dict__.items():
            if self is obj:
                return name
        raise GeniviConverterCanNotClarifyNameException()

    def __get__(self, instance, owner):
        return {
            self._get_name(owner=owner): self._get_value(instance=instance)
        }

    def _get_value(self, instance):
        value = instance.data.get(self._src_name)
        if value is None:
            value = self.NONE_DEFAULT_VALUE
        else:
            value = self._convert_value(instance=instance, value=value)
        return value

    def _convert_value(self, instance, value):
        return value
