import argparse
import time

import can
from piper_sdk import C_PiperInterface_V2

from piper_cli.protocols import disable_arm_msg, motion_ctrl_2_msg


def command_disable(args: argparse.Namespace) -> None:
    with can.Bus(channel=args.can_interface, interface="socketcan") as bus:
        piper = C_PiperInterface_V2(args.can_interface)
        piper.ConnectPort()

        bus.send(motion_ctrl_2_msg(move_mode="joint", move_speed_rate=20))
        time.sleep(0.1)

        positions = [0, 0, 0, 0, 17000, 0]
        piper.JointCtrl(*positions)

        done = False
        tolerance = 1000
        while not done:
            time.sleep(0.1)
            state = piper.GetArmJointMsgs().joint_state
            done = all(
                [
                    abs(state.joint_1 - positions[0]) <= tolerance,
                    abs(state.joint_2 - positions[1]) <= tolerance,
                    abs(state.joint_3 - positions[2]) <= tolerance,
                    abs(state.joint_4 - positions[3]) <= tolerance,
                    abs(state.joint_5 - positions[4]) <= tolerance,
                    abs(state.joint_6 - positions[5]) <= tolerance,
                ]
            )

        bus.send(disable_arm_msg())


__all__ = ["command_disable"]
