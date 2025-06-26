from typing import Literal

import can

ENABLE_ARM_ID = 0x471


def disable_arm_msg(motor_num: Literal[1, 2, 3, 4, 5, 6, 7] = 7) -> can.Message:
    data = [motor_num, 0x01, 0x00, 0x00, 0x00, 0x00]
    return can.Message(arbitration_id=ENABLE_ARM_ID, data=data, is_extended_id=False)


def enable_arm_msg(motor_num: Literal[1, 2, 3, 4, 5, 6, 7] = 7) -> can.Message:
    data = [motor_num, 0x02, 0x00, 0x00, 0x00, 0x00]
    return can.Message(arbitration_id=ENABLE_ARM_ID, data=data, is_extended_id=False)


__all__ = ["disable_arm_msg", "enable_arm_msg"]
