# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# pylint: disable=line-too-long
"""Check for conflicts with 'autogen-agentchat' package."""

import sys
from importlib.metadata import PackageNotFoundError, version


# fmt: off
def check_conflicts() -> None:  # pragma: no cover
    """Check for conflicts with 'autogen-agentchat' package."""
    try:
        version("autogen-agentchat")
        print(
            "Conflict detected: 'autogen-agentchat' is installed "
            "in the current environment, \n"
            "which conflicts with 'ag2' / 'pyautogen'.\n"
            "Please uninstall 'autogen-agentchat': \n"
            f"{sys.executable} -m pip uninstall -y autogen-agentchat" + "\n"
            "And install 'pyautogen' (and/or 'waldiez') again: \n"
            f"{sys.executable} -m pip install --force pyautogen waldiez"
        )
        sys.exit(1)
    except PackageNotFoundError:
        pass

# fmt: on
