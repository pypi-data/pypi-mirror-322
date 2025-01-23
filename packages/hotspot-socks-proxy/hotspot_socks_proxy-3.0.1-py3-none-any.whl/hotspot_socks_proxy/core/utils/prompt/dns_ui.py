"""DNS-specific UI components."""

import time
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from .prompt import PromptHandler

console = Console()

class DNSUI(PromptHandler):
    """UI handler for DNS resolution."""
    
    def __init__(self):
        super().__init__()
        self._spinner = Spinner('dots', text='')
        self._last_query = None
        self._query_time = 0
        self._cache_hits = 0
        self._cache_misses = 0
        
    def log_resolution(self, domain: str, ip: str, cache_hit: bool, duration: float):
        """Log a DNS resolution event."""
        self._last_query = (domain, ip)
        self._query_time = duration
        if cache_hit:
            self._cache_hits += 1
        else:
            self._cache_misses += 1
            
    def _generate_table(self) -> Table:
        """Generate DNS statistics table."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="green", no_wrap=True)
        
        if self._last_query:
            domain, ip = self._last_query
            table.add_row("Last Query", f"{domain} → {ip}")
            table.add_row("Resolution Time", f"{self._query_time:.3f}s")
        
        table.add_row("Cache Hits", str(self._cache_hits))
        table.add_row("Cache Misses", str(self._cache_misses))
        
        if self._cache_hits + self._cache_misses > 0:
            hit_rate = self._cache_hits / (self._cache_hits + self._cache_misses) * 100
            table.add_row("Cache Hit Rate", f"{hit_rate:.1f}%")
            
        return table
        
    def _generate_display(self) -> Panel:
        """Generate the main display panel."""
        title = Text("DNS Resolution Statistics", style="bold cyan")
        table = self._generate_table()
        return Panel(
            table,
            title=title,
            border_style="blue",
            padding=(1, 2)
        )

# Global UI instance
dns_ui = DNSUI()
