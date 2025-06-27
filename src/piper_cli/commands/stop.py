import argparse

from piper_sdk import C_PiperInterface_V2


def command_stop(args: argparse.Namespace) -> None:
    piper = C_PiperInterface_V2(args.can_interface)
    piper.ConnectPort()
    piper.MotionCtrl_1(0x2, 0x0, 0x0)


__all__ = ["command_stop"]
