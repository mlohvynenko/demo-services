#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from abc import ABCMeta, abstractmethod


class EmulatorUpdaterBase(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        self._to_rectangle = None
        self._rectangle = None
        self._vehicle_stop = None
        self._vehicle_tire_break = False

    @abstractmethod
    def update(self, *args, **kwargs):
        pass
