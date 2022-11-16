import logging
from typing import List, Tuple

from proxy.apps.resolver import resolver


class SSHBastionResolver(resolver.BaseResolver):
    """Resolve SNI and ALPN and return the upstream address"""

    _logger = logging.getLogger(__name__)

    # def __init__(self, base_domain: str, ssh_tunnel: SSHTunnel) -> None:
    def __init__(self, base_domain: str, ssh_tunnel: any) -> None:
        super().__init__()
        self._base_domain = base_domain

    async def _resolve(self, sni: str, alpn: str) -> Tuple[str, int]:
        # base = self._base_domain.split(".")
        # resource = sni.split('.')[-len(base)]

        # self._logger.info(f"Connecting to '{resource}' Tunnel")

        # # SSHTunnel(sni.split(".")[0]).connect()

        # if alpn in ['http/1.1', 'h2']:
        #     return "127.0.0.1", 8000    # to do test with 'python -m http.server'

        return "127.0.0.1", 22  # forward traffic to ssh server

    @property
    def accepted_protocols(self) -> List[str]:
        return ["http/1.1", "h2", "ssh"]
