"""DNS resolution handler with fallback mechanisms.

This module provides robust DNS resolution with:
- Multiple resolver strategies
- Configurable nameservers
- Fallback mechanisms
- Caching support
- Timeout handling
- Error reporting

The handler uses a combination of system DNS and public DNS servers
to ensure reliable domain resolution even when the primary DNS fails.

Example:
    resolver = DNSResolver()
    try:
        ip = resolver.resolve("example.com")
        print(f"Resolved IP: {ip}")
    except DNSResolutionError as e:
        print(f"Failed to resolve: {e}")
"""

import socket
from functools import lru_cache
from typing import Optional
import time

import dns.resolver
from rich.console import Console

from ..exceptions import DNSResolutionError
from ..utils.prompt.dns_ui import dns_ui

console = Console()

class DNSResolver:
    """DNS resolver with fallback mechanisms and caching."""
    
    def __init__(self):
        # Default public DNS servers
        self.public_nameservers = [
            "1.1.1.1",        # Cloudflare
            "8.8.8.8",        # Google
            "9.9.9.9",        # Quad9
            "208.67.222.222"  # OpenDNS
        ]
        
        # Initialize resolver with system defaults
        self.resolver = dns.resolver.Resolver()
        
        # Keep original nameservers as fallback
        self.system_nameservers = self.resolver.nameservers.copy()
        
        # Configure timeouts
        self.resolver.timeout = 1.0    # Timeout for each query
        self.resolver.lifetime = 3.0   # Total timeout for all queries
        self.resolver.tries = 2        # Number of retries per nameserver

    @lru_cache(maxsize=1024, ttl=300)  # Cache results for 5 minutes
    def resolve(self, domain: str) -> str:
        """Resolve domain name to IP address using multiple strategies.
        
        Args:
            domain: Domain name to resolve
            
        Returns:
            Resolved IP address as string
            
        Raises:
            DNSResolutionError: If resolution fails with all methods
        """
        start_time = time.monotonic()
        try:
            # Try cache first
            if hasattr(self.resolve, 'cache_info'):
                result = self.resolve.__wrapped__(self, domain)
                cache_info = self.resolve.cache_info()
                cache_hit = cache_info.hits > 0
            else:
                result = self._resolve_uncached(domain)
                cache_hit = False
                
            duration = time.monotonic() - start_time
            dns_ui.log_resolution(domain, result, cache_hit, duration)
            return result
            
        except Exception as e:
            duration = time.monotonic() - start_time
            dns_ui.log_resolution(domain, "Failed", False, duration)
            raise

    def _resolve_uncached(self, domain: str) -> str:
        """Resolve domain name to IP address using multiple strategies.
        
        Args:
            domain: Domain name to resolve
            
        Returns:
            Resolved IP address as string
            
        Raises:
            DNSResolutionError: If resolution fails with all methods
        """
        # Strategy 1: Try system resolver first (fastest)
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            pass

        # Strategy 2: Try public DNS servers one by one
        errors = []
        for ns in self.public_nameservers:
            try:
                # Configure resolver to use this nameserver
                self.resolver.nameservers = [ns]
                
                # Attempt resolution
                answer = self.resolver.resolve(domain, "A")
                if answer:
                    return str(answer[0])
            except dns.resolver.NXDOMAIN:
                # Domain doesn't exist, no point trying other servers
                raise DNSResolutionError(f"Domain {domain} does not exist")
            except dns.resolver.NoAnswer:
                # No A record, try next server
                continue
            except Exception as e:
                errors.append(f"{ns}: {str(e)}")
                continue

        # Strategy 3: Final attempt with system nameservers
        try:
            self.resolver.nameservers = self.system_nameservers
            answer = self.resolver.resolve(domain, "A")
            if answer:
                return str(answer[0])
        except Exception as e:
            errors.append(f"System DNS: {str(e)}")

        # All strategies failed
        error_msg = f"DNS resolution failed for {domain}. Errors: {'; '.join(errors)}"
        raise DNSResolutionError(error_msg)

# Global resolver instance
dns_resolver = DNSResolver()
