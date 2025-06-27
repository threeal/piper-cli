import argparse
import warnings

from .commands import command_disable, command_enable, command_stop, command_teleop

warnings.filterwarnings("ignore", category=SyntaxWarning, module=r"^piper_sdk(\.|$)")


def main() -> None:
    parser = argparse.ArgumentParser(prog="piper")
    parser.add_argument("-v", "--version", action="version", version="0.1.0")
    subparsers = parser.add_subparsers(required=True)

    disable_parser = subparsers.add_parser("disable", help="disable the PiPER arm")
    disable_parser.set_defaults(func=command_disable)
    disable_parser.add_argument("can_interface", help="CAN interface to use")

    enable_parser = subparsers.add_parser("enable", help="enable the PiPER arm")
    enable_parser.set_defaults(func=command_enable)
    enable_parser.add_argument("can_interface", help="CAN interface to use")

    stop_parser = subparsers.add_parser("stop", help="emergency stop the PiPER arm")
    stop_parser.set_defaults(func=command_stop)
    stop_parser.add_argument("can_interface", help="CAN interface to use")

    teleop_parser = subparsers.add_parser(
        "teleop", help="teleop and record the PiPER arm"
    )
    teleop_parser.set_defaults(func=command_teleop)
    teleop_parser.add_argument("leader_can", help="CAN interface of the leader to use")
    teleop_parser.add_argument(
        "follower_can", help="CAN interface of the follower to use"
    )
    teleop_parser.add_argument("prefix_name", help="prefix name of record data")

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
