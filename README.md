# Piper CLI

A command line interface for [AgileX PiPER](https://global.agilex.ai/products/piper) robotic arm.

## How to Use

1. Install [uv](https://docs.astral.sh/uv/).
2. Install the dependencies:

   ```bash
   uv sync
   ```
3. To run teleoperation, first enable the follower arm, then start the teleop program:

   ```bash
   uv run piper enable can0
   uv run piper teleop can3 can0 .records/my_record
   ```

## License

This project is licensed under the terms of the [MIT License](./LICENSE).

Copyright © 2025 [Alfi Maulana](https://github.com/threeal)
