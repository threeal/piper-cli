# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `piper-kit`, an SDK and CLI tools for the AgileX PiPER robotic arm. The project provides Python bindings for controlling the robotic arm via CAN bus interface using the `python-can` library.

## Development Commands

**Package Management:**
- `uv sync` - Install dependencies
- `uv run piper --help` - Run the CLI tool

**Code Quality:**
- `uv run ruff format` - Format code
- `uv run ruff check` - Run linter
- `uv run ruff check --fix` - Auto-fix linting issues

**Git Hooks:**
- Uses `lefthook` for pre-commit hooks that automatically format and lint code

## Architecture

**Core Components:**
- `PiperInterface` (`src/piper_kit/interface.py`) - Main interface class for communicating with the PiPER arm via CAN bus
- CLI commands (`src/piper_kit/_cli/`) - `enable` and `disable` commands for arm control (private module)
- Message system (`src/piper_kit/messages/`) - CAN message definitions split into `transmit` and `receive` modules

**Message Architecture:**
- **Transmit messages:** Joint control, motion control, and joint enable/disable commands
- **Receive messages:** Joint feedback, motor info, and unknown message handling
- Messages are organized by function with separate classes for different joint pairs (12, 34, 56)

**CAN Bus Communication:**
- Uses socketcan interface (default: `can0`)
- All communication is synchronous with blocking reads
- Context manager pattern for proper bus cleanup

**CLI Structure:**
- Entry point: `piper` command with subcommands
- `piper enable [can_interface]` - Enable arm and set to home position
- `piper disable [can_interface]` - Move to safe position and disable arm
- Default CAN interface is `can0` if not specified

## Key Implementation Details

- Joint positions are controlled in pairs (joints 1-2, 3-4, 5-6)
- Motor status monitoring ensures joints are properly enabled before motion
- Disable sequence includes moving to safe position before powering down
- All joint operations include feedback validation with tolerance checking