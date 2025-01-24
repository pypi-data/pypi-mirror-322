"""Network routing utilities."""

import contextlib
import platform
import subprocess
from typing import Final

from loguru import logger
from rich.console import Console

console = Console()

# Determine OS and available commands
IS_MACOS: Final = platform.system() == "Darwin"

def setup_routing(interface: str, interface_ip: str) -> bool:
    """Set up routing for the proxy interface."""
    try:
        if IS_MACOS:
            # Enable IP forwarding on macOS
            subprocess.run(
                ["sysctl", "-w", "net.inet.ip.forwarding=1"],
                check=True,
                capture_output=True,
                text=True,
            )
            
            # Create temporary PF rules file with more specific routing
            pf_rules = f"""
# SOCKS proxy forwarding rules
nat-anchor "com.apple/*"
rdr-anchor "com.apple/*"
nat on {interface} from any to any -> ({interface})
rdr pass on lo0 proto tcp from any to any port 9050 -> 127.0.0.1 port 9050
pass in quick on {interface} all
pass out quick on {interface} all
pass in quick proto tcp from any to any port 9050
pass out quick from ({interface}) to any keep state
"""
            rules_file = "/tmp/proxy_pf.conf"
            with open(rules_file, "w") as f:
                f.write(pf_rules)
            
            # Flush existing rules and enable PF
            subprocess.run(["pfctl", "-F", "all"], capture_output=True)
            subprocess.run(["pfctl", "-e"], capture_output=True)
            
            # Load our rules
            result = subprocess.run(
                ["pfctl", "-f", rules_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0 and "No ALTQ support" not in result.stderr:
                logger.error(f"PF configuration error: {result.stderr}")
                return False
                
            return True
            
        else:  # Linux
            # Enable IP forwarding
            subprocess.run(
                ["sysctl", "-w", "net.ipv4.ip_forward=1"],
                check=True,
                capture_output=True,
                text=True,
            )

            # Add routing rules using ip command
            subprocess.run(
                ["ip", "route", "add", "default", "via", interface_ip, "dev", interface, "table", "200"],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["ip", "rule", "add", "from", interface_ip, "table", "200"],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["ip", "rule", "add", "fwmark", "1", "table", "200"],
                check=True,
                capture_output=True,
                text=True,
            )

            return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting up routing: {e.stderr}")
        console.print(f"[red]Error setting up routing: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error setting up routing: {e}")
        console.print(f"[red]Error setting up routing: {e}")
        return False

def cleanup_routing(interface_ip: str) -> None:
    """Clean up routing rules."""
    try:
        if IS_MACOS:
            # Disable IP forwarding
            subprocess.run(
                ["sysctl", "-w", "net.inet.ip.forwarding=0"],
                check=True,
                capture_output=True,
            )
            # Disable PF
            with contextlib.suppress(subprocess.CalledProcessError):
                subprocess.run(["pfctl", "-d"], check=True, capture_output=True)
        else:
            # Clean up Linux routing rules
            with contextlib.suppress(subprocess.CalledProcessError):
                subprocess.run(
                    ["ip", "rule", "del", "from", interface_ip, "table", "200"],
                    check=True,
                    capture_output=True,
                )
    except Exception as e:
        logger.error(f"Error cleaning up routing: {e}")
