#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telemetry_emulator.genivi.fields import (
    BaseGeniviConverter, SpeedGeniviConverter, FuelLevelGeniviConverter, SeatBeltGeniviConverter,
    TurnLight, TurnLightGeniviConverter, TurnLightLeverGeniviConverter, PedalBrakeGeniviConverter,
    BooleanFalseGeniviConverter, CoordinateConverter, BeamConverter, PressureKPAToPSIConverter,
    ParkingBrakeGeniviConverter, DoorLockConverter
)


class GeniviCloudConverter:
    FUEL_TANK_SIZE_GAL = 18

    # Location
    lat = CoordinateConverter(src_name="Signal.Cabin.Infotainment.Navigation.CurrentLocation.Latitude")
    lon = CoordinateConverter(
        src_name="Signal.Cabin.Infotainment.Navigation.CurrentLocation.Longitude",
        multiplier=1
    )

    # Engine
    engrpm = BaseGeniviConverter(src_name="Signal.Drivetrain.InternalCombustionEngine.Engine.Speed")
    engcooltemp = BaseGeniviConverter(src_name="Signal.OBD.CoolantTemperature")

    # Vehicle
    gr = BaseGeniviConverter(src_name="Signal.Drivetrain.Transmission.Gear")
    veh_speed = SpeedGeniviConverter(src_name="Signal.Vehicle.Speed")
    vehspddisp = SpeedGeniviConverter(src_name="Signal.Vehicle.Speed")
    lrw = BaseGeniviConverter(src_name="Signal.Chassis.SteeringWheel.Angle")
    avgfuellvl = FuelLevelGeniviConverter(src_name="Signal.Drivetrain.FuelSystem.Level")

    # Breaks
    brk_stat = PedalBrakeGeniviConverter(src_name="Signal.Chassis.Brake.PedalPosition")
    prkbrkstat = ParkingBrakeGeniviConverter(src_name="Signal.Chassis.ParkingBrake.IsEngaged")

    # Doors
    drv_ajar = BooleanFalseGeniviConverter(src_name="Signal.Cabin.Door.Row1.Left.IsOpen")
    psg_ajar = BooleanFalseGeniviConverter(src_name="Signal.Cabin.Door.Row1.Right.IsOpen")
    l_r_ajar = BooleanFalseGeniviConverter(src_name="Signal.Cabin.Door.Row2.Left.IsOpen")
    r_r_ajar = BooleanFalseGeniviConverter(src_name="Signal.Cabin.Door.Row2.Right.IsOpen")
    rr_dr_unlkd = BooleanFalseGeniviConverter(src_name="Signal.Body.Trunk.IsOpen")
    dr_lk_stat = DoorLockConverter(
        fl="Signal.Cabin.Door.Row1.Left.IsLocked",
        fr="Signal.Cabin.Door.Row1.Right.IsLocked",
        rl="Signal.Cabin.Door.Row2.Left.IsLocked",
        rr="Signal.Cabin.Door.Row2.Right.IsLocked"
    )

    # Belts
    drv_seatbelt = SeatBeltGeniviConverter(src_name="Signal.Cabin.Seat.Row1.Pos1.IsBelted")
    psg_seatbelt = SeatBeltGeniviConverter(src_name="Signal.Cabin.Seat.Row1.Pos2.IsBelted")

    # Lights
    hazard_status = BooleanFalseGeniviConverter(src_name="Signal.Body.Lights.IsHazardOn")
    turnind_lt_on = TurnLightGeniviConverter(src_name="Signal.Traffic.Turn.Direction", side=TurnLight.LEFT)
    turnind_rt_on = TurnLightGeniviConverter(src_name="Signal.Traffic.Turn.Direction", side=TurnLight.RIGHT)
    turnindlvr_stat = TurnLightLeverGeniviConverter(
        src_name="Signal.Traffic.Turn.Direction",
        hazard_src="Signal.Body.Lights.IsHazardOn"
    )
    hibmlvr_stat = BeamConverter(src_name="Signal.Body.Lights.IsHighBeamOn")

    # Conditions
    veh_int_temp = BaseGeniviConverter(src_name="Signal.Cabin.HVAC.AmbientAirTemperature")

    # Wheels
    tirepressfl = PressureKPAToPSIConverter(src_name="Signal.Chassis.Axle.Row1.Wheel.Left.Tire.Pressure")
    tirepressfr = PressureKPAToPSIConverter(src_name="Signal.Chassis.Axle.Row1.Wheel.Right.Tire.Pressure")
    tirepressrl = PressureKPAToPSIConverter(src_name="Signal.Chassis.Axle.Row2.Wheel.Left.Tire.Pressure")
    tirepressrr = PressureKPAToPSIConverter(src_name="Signal.Chassis.Axle.Row2.Wheel.Right.Tire.Pressure")

    def __init__(self, src_data):
        self._data = src_data

    @property
    def data(self):
        return self._data

    def get_converted_values(self):
        result = {}
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, BaseGeniviConverter):
                result.update(getattr(self, name))

        return result
