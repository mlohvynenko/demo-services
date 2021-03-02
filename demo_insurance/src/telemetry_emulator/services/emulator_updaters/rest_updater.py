#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from telemetry_emulator.services.emulator_updaters.base import EmulatorUpdaterBase


class EmulatorNotDefinedException(Exception):
    pass


class RESTUpdater(EmulatorUpdaterBase):

    def __init__(self, emulator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not emulator:
            raise EmulatorNotDefinedException()
        self._emulator = emulator

    def update(self, rectangle_long0=None, rectangle_lat0=None, rectangle_long1=None,
               rectangle_lat1=None, to_rectangle=None, stop=None, tire_break=False, *args, **kwargs):
        if all((rectangle_long0, rectangle_lat0, rectangle_long1, rectangle_lat1,)):
            self._emulator.set_rectangle(
                long0=rectangle_long0,
                lat0=rectangle_lat0,
                long1=rectangle_long1,
                lat1=rectangle_lat1
            )
        else:
            self._emulator.del_rectangle()

        if to_rectangle is not None:
            self._emulator.set_rectangle_direction(target=to_rectangle)

        if stop is not None and stop != self._vehicle_stop:
            self._vehicle_stop = bool(stop)
            if stop:
                self._emulator.command_stop()
            else:
                self._emulator.command_go()

        if tire_break != self._vehicle_tire_break:
            self._vehicle_tire_break = bool(tire_break)
            if tire_break:
                self._emulator.tire_break()
