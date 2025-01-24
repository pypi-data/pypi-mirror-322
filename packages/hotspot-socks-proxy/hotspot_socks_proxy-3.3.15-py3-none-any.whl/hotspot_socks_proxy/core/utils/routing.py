"""Network routing utilities."""

import contextlib
import shutil
import subprocess
from typing import Final

from loguru import logger
from rich.console import Console

console = Console()

# Find full path to ip command
IP_CMD: Final = shutil.which("ip")
if not IP_CMD:
    msg = "'ip' command not found in PATH"
    raise RuntimeError(msg)

def setup_routing(interface: str, interface_ip: str) -> bool:
    """Set up routing for the proxy interface."""
    try:
        # Enable IP forwarding
        subprocess.run(
            ["sysctl", "-w", "net.ipv4.ip_forward=1"],
            check=True,
            capture_output=True,
            text=True,
        )

        # Add a new routing table for our interface
        subprocess.run(
            [IP_CMD, "route", "add", "default", "via", interface_ip, "dev", interface, "table", "200"],
            check=True,
            capture_output=True,
            text=True,
        )

        # Add rule to use this table for traffic from our IP
        subprocess.run(
            [IP_CMD, "rule", "add", "from", interface_ip, "table", "200"],
            check=True,
            capture_output=True,
            text=True,
        )

        # Add rule to mark packets going through our interface
        subprocess.run(
            [IP_CMD, "rule", "add", "fwmark", "1", "table", "200"],
            check=True,
            capture_output=True,
            text=True,
        )

        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting up routing: {e.stderr}")
        console.print(f"[red]Error setting up routing: {e.stderr}")
        return False

def cleanup_routing(interface_ip: str) -> None:
    """Clean up routing rules."""
    with contextlib.suppress(subprocess.CalledProcessError):
        subprocess.run(
            [IP_CMD, "rule", "del", "from", interface_ip, "table", "200"],
            check=True,
            capture_output=True,
            text=True,
        )
