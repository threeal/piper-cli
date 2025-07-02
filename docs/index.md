# PiPER Kit

## CLI Usage

### Enable Arm

```bash
piper enable [can_interface]
```

Enables the PiPER arm and moves it to the home position. The CAN interface defaults to `can0` if not specified.

### Disable Arm

```bash
piper disable [can_interface]
```

Moves the PiPER arm to a safe position and disables all joints. The CAN interface defaults to `can0` if not specified.

## API Reference

### Main Interface

::: piper_kit.PiperInterface

### Message Classes

#### Transmit Messages

::: piper_kit.messages.TransmitMessage
::: piper_kit.messages.EnableJointMessage
::: piper_kit.messages.MotionControlBMessage
::: piper_kit.messages.JointControl12Message
::: piper_kit.messages.JointControl34Message
::: piper_kit.messages.JointControl56Message

#### Receive Messages

::: piper_kit.messages.ReceiveMessage
::: piper_kit.messages.MotorInfoBMessage
::: piper_kit.messages.JointFeedback12Message
::: piper_kit.messages.JointFeedback34Message
::: piper_kit.messages.JointFeedback56Message
::: piper_kit.messages.UnknownMessage