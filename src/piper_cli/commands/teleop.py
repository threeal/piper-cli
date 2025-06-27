import argparse
import ctypes
import os
import shutil
import struct
import threading
import time

import can
import cv2


def bytes_to_int32(data: bytes) -> int:
    num = int.from_bytes(data) & 0xFFFFFFFF
    if num & 0x80000000:
        num -= 0x100000000
    return num


def int32_to_bytes(num: int) -> bytes:
    value = ctypes.c_int32(num).value
    return struct.unpack("BBBB", struct.pack(">i", value))


def command_teleop(args: argparse.Namespace) -> None:
    os.makedirs(os.path.dirname(args.prefix_name), exist_ok=True)

    def video_capture():
        shutil.rmtree(f"{args.prefix_name}_captures", ignore_errors=True)
        os.makedirs(f"{args.prefix_name}_captures", exist_ok=True)

        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                filename = os.path.join(
                    f"{args.prefix_name}_captures", f"{time.time()}.png"
                )
                cv2.imwrite(filename, frame)

    thread = threading.Thread(target=video_capture)
    thread.start()

    with (
        can.Bus(channel=args.leader_can, interface="socketcan") as leader,
        can.Bus(channel=args.follower_can, interface="socketcan") as follower,
        open(f"{args.prefix_name}_leader_read.csv", "w") as leader_read_file,
        open(f"{args.prefix_name}_follower_read.csv", "w") as follower_read_file,
    ):
        leader_read_file.write(
            "timestamp,joint_1,joint_2,joint_3,joint_4,joint_5,joint_6,gripper\n"
        )

        follower_read_file.write(
            "timestamp,joint_1,joint_2,joint_3,joint_4,joint_5,joint_6,gripper\n"
        )

        def follower_read():
            for msg in follower:
                if msg.arbitration_id == 0x2A5:
                    joints = [
                        bytes_to_int32(msg.data[0:4]),
                        bytes_to_int32(msg.data[4:8]),
                    ]
                    follower_read_file.write(
                        f"{time.time()},{joints[0]},{joints[1]},,,,,\n"
                    )

                if msg.arbitration_id == 0x2A6:
                    joints = [
                        bytes_to_int32(msg.data[0:4]),
                        bytes_to_int32(msg.data[4:8]),
                    ]
                    follower_read_file.write(
                        f"{time.time()},,,{joints[0]},{joints[1]},,,\n"
                    )

                if msg.arbitration_id == 0x2A7:
                    joints = [
                        bytes_to_int32(msg.data[0:4]),
                        bytes_to_int32(msg.data[4:8]),
                    ]
                    follower_read_file.write(
                        f"{time.time()},,,,,{joints[0]},{joints[1]},\n"
                    )

                if msg.arbitration_id == 0x2A8:
                    gripper = bytes_to_int32(msg.data[0:4])
                    follower_read_file.write(f"{time.time()},,,,,,,{gripper}\n")

        thread = threading.Thread(target=follower_read)
        thread.start()

        for msg in leader:
            if msg.arbitration_id == 0x2A5:
                joints = [bytes_to_int32(msg.data[0:4]), bytes_to_int32(msg.data[4:8])]
                leader_read_file.write(f"{time.time()},{joints[0]},{joints[1]},,,,,\n")

                follower.send(
                    can.Message(
                        arbitration_id=0x155, data=msg.data, is_extended_id=False
                    )
                )

            if msg.arbitration_id == 0x2A6:
                joints = [bytes_to_int32(msg.data[0:4]), bytes_to_int32(msg.data[4:8])]
                leader_read_file.write(f"{time.time()},,,{joints[0]},{joints[1]},,,\n")

                follower.send(
                    can.Message(
                        arbitration_id=0x156, data=msg.data, is_extended_id=False
                    )
                )

            if msg.arbitration_id == 0x2A7:
                joints = [bytes_to_int32(msg.data[0:4]), bytes_to_int32(msg.data[4:8])]
                leader_read_file.write(f"{time.time()},,,,,{joints[0]},{joints[1]},\n")

                follower.send(
                    can.Message(
                        arbitration_id=0x157, data=msg.data, is_extended_id=False
                    )
                )

            if msg.arbitration_id == 0x2A8:
                gripper = bytes_to_int32(msg.data[0:4])
                leader_read_file.write(f"{time.time()},,,,,,,{gripper}\n")

                follower.send(
                    can.Message(
                        arbitration_id=0x159,
                        data=[*int32_to_bytes(gripper), 0x03, 0xE8, 0x01, 0x00],
                        is_extended_id=False,
                    )
                )


__all__ = ["command_teleop"]
