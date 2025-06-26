import argparse
import time

import can
from piper_sdk import C_PiperInterface_V2

from piper_cli.protocols import (
    enable_arm_msg,
    is_low_spd_info_msg,
    motion_ctrl_2_msg,
    parse_low_spd_info_msg,
)


def command_enable(args: argparse.Namespace) -> None:
    with can.Bus(channel=args.can_interface, interface="socketcan") as bus:
        bus.send(enable_arm_msg())

        piper = C_PiperInterface_V2(args.can_interface)
        piper.ConnectPort()

        enabled = [False] * 6
        while not all(enabled):
            msg = bus.recv()
            if is_low_spd_info_msg(msg):
                info = parse_low_spd_info_msg(msg)
                enabled[info.joint_id - 1] = info.driver_status.driver_enabled

        bus.send(motion_ctrl_2_msg(move_mode="joint", move_speed_rate=20))
        time.sleep(0.1)

        piper.JointCtrl(0, 0, 0, 0, 0, 0)


__all__ = ["command_enable"]
