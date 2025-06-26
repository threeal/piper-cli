from typing import Literal

import can

MOTION_CTRL_2_ID = 0x151


def motion_ctrl_2_msg(
    *,
    ctrl_mode: Literal["standby", "can", "ethernet", "wifi", "offline"] = "can",
    move_mode: Literal["position", "joint", "linear", "circular"] = "joint",
    move_speed_rate: int = 50,
) -> can.Message:
    ctrl_mode_code = 0x00
    if ctrl_mode == "can":
        ctrl_mode_code = 0x01
    elif ctrl_mode == "ethernet":
        ctrl_mode_code = 0x03
    elif ctrl_mode == "wifi":
        ctrl_mode_code = 0x04
    elif ctrl_mode == "offline":
        ctrl_mode_code = 0x07

    move_mode_code = 0x00
    if move_mode == "joint":
        move_mode_code = 0x01
    elif move_mode == "linear":
        move_mode_code = 0x02
    elif move_mode == "circular":
        move_mode_code = 0x03

    data = [
        ctrl_mode_code,
        move_mode_code,
        move_speed_rate,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]

    return can.Message(arbitration_id=MOTION_CTRL_2_ID, data=data, is_extended_id=False)


__all__ = ["motion_ctrl_2_msg"]
