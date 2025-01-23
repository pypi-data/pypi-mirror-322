"""Custom exceptions for the proxy server."""


class ProxyError(Exception):
    """Base exception for proxy errors."""


class DNSResolutionError(ProxyError):
    """Raised when DNS resolution fails."""
