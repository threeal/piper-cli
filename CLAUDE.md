# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python SDK and CLI toolkit for controlling the AgileX PiPER 6-DOF robotic arm with gripper via CAN bus communication. The package provides direct low-level control through socketcan interface with real-time joint positioning, gripper control, motion control, and safety monitoring capabilities.

## Development Commands

### Setup and Dependencies
```bash
# Install dependencies for development
uv sync

# Install for development (from source)
uv sync
```

### Code Quality
```bash
# Format code
uv run ruff format

# Lint and fix issues
uv run ruff check --fix

# Run both formatting and linting (as done in pre-commit)
uv run ruff format && uv run ruff check --fix
```

### Testing CLI Commands
```bash
# Test CLI commands (requires CAN interface)
uv run piper enable [can_interface]
uv run piper disable [can_interface]
uv run piper teleop joint [can_interface]
```

## Architecture

### Core Components

1. **PiperInterface** (`src/piper_kit/interface.py`): Main interface class that provides:
   - Context manager for automatic CAN bus resource cleanup
   - Joint control methods (individual and batch control for 6 joints)
   - Gripper control methods (position, effort, enable/disable)
   - Motion control configuration
   - Message reading and feedback collection
   - Enable/disable functionality for individual joints or all joints

2. **CLI Module** (`src/piper_kit/_cli/`): Command-line interface with subcommands:
   - `enable`: Moves arm to home position and enables joints and gripper
   - `disable`: Moves arm to safe position and disables joints and gripper
   - `teleop joint`: Real-time joint teleoperation

3. **Message System** (`src/piper_kit/messages/`): CAN message protocol implementation:
   - **Transmit messages**: Joint control, gripper control, motion control, enable/disable commands
   - **Receive messages**: Joint feedback, motor info, unknown message handling
   - Uses message ID-based routing for different message types

### Key Design Patterns

- **Context Manager Pattern**: PiperInterface implements `__enter__`/`__exit__` for automatic CAN bus cleanup
- **Message Factory Pattern**: `read_message()` routes incoming CAN messages to appropriate message classes based on arbitration ID
- **Batch Operations**: Joint control can be done individually (joints 1-2, 3-4, 5-6) or all at once
- **Type Safety**: Uses Python typing and literal types for joint IDs and control modes

### CAN Bus Communication

The system communicates with the robotic arm using specific CAN message IDs:
- Joint control messages are sent in pairs (1-2, 3-4, 5-6)
- Gripper control messages (ID 0x159) control position and effort
- Feedback messages return current joint positions
- Motor info messages provide diagnostic information
- All communication goes through the socketcan interface

## Development Notes

- Uses `uv` for dependency management and project setup
- Follows strict linting rules with ruff (all rules enabled except COM812, D203, D213)
- Pre-commit hooks automatically format and lint code
- CLI entry point is configured in pyproject.toml as `piper` command
- Requires Python 3.13+ and `python-can` library for CAN bus communication
