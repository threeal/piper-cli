import can

LOW_SPD_INFO_1_ID = 0x261
LOW_SPD_INFO_6_ID = 0x266


class LowSpdInfoMsg:
    class DriverStatus:
        def __init__(self, driver_status_code: int) -> None:
            self.low_voltage = driver_status_code & 1 != 0
            self.motor_overheating = driver_status_code & 2 != 0
            self.driver_overcurrent = driver_status_code & 4 != 0
            self.driver_overheating = driver_status_code & 8 != 0
            self.collision_triggered = driver_status_code & 16 != 0
            self.driver_error = driver_status_code & 32 != 0
            self.driver_enabled = driver_status_code & 64 != 0
            self.stalling_triggered = driver_status_code & 128 != 0

    def __init__(  # noqa: PLR0913
        self,
        *,
        joint_id: int,
        bus_voltage: int,
        driver_temp: int,
        motor_temp: int,
        driver_status_code: int,
        bus_current: int,
    ) -> None:
        self.joint_id = joint_id
        self.bus_voltage = bus_voltage
        self.driver_temp = driver_temp
        self.motor_temp = motor_temp
        self.driver_status = LowSpdInfoMsg.DriverStatus(driver_status_code)
        self.bus_current = bus_current


def is_low_spd_info_msg(msg: can.Message) -> bool:
    return LOW_SPD_INFO_1_ID <= msg.arbitration_id <= LOW_SPD_INFO_6_ID


def parse_low_spd_info_msg(msg: can.Message) -> LowSpdInfoMsg:
    return LowSpdInfoMsg(
        joint_id=msg.arbitration_id - LOW_SPD_INFO_1_ID + 1,
        bus_voltage=int.from_bytes(msg.data[0:2]),
        driver_temp=int.from_bytes(msg.data[2:4], signed=True),
        motor_temp=int.from_bytes(msg.data[4:5], signed=True),
        driver_status_code=int.from_bytes(msg.data[5:6]),
        bus_current=int.from_bytes(msg.data[6:8]),
    )


__all__ = ["LowSpdInfoMsg", "is_low_spd_info_msg", "parse_low_spd_info_msg"]
