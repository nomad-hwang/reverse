import logging
from asyncio import StreamReader, StreamWriter
from typing import List, Tuple

from proxy.apps.bastion.bastion import get_all_device, get_open_tunnels, get_port
from proxy.apps.resolver import resolver
from proxy.apps.socks5.socks5 import create_connection
from proxy.config import config


class SSHBastionResolver(resolver.BaseResolver):
    """Resolve SNI and ALPN and return the upstream address"""

    _logger = logging.getLogger(__name__)

    def __init__(self, base_domain: str) -> None:
        super().__init__()
        self._base_domain = base_domain

    async def _routed_connection(
        self, sni: str, alpn: str
    ) -> tuple[StreamReader, StreamWriter]:
        # Resolve example when base_domain is bastion.example.com
        # if sni == "device1.bastion.example.com" then target = "device1"
        # if sni == "test.device2.bastion.example.com" then target = "device2"

        url = sni.split(self._base_domain)[0].rstrip(".")
        target = url.split(".")[-1]

        self._logger.info(f"Connecting to '{target}' Tunnel")

        port = 8000
        if alpn == "":
            port = 22

        return await create_connection(
            socks_host=config.BASTION_TUNNEL_HOST,
            socks_port=await get_port(target),
            host="127.0.0.1",
            port=port,
        )

    @property
    def accepted_protocols(self) -> List[str]:
        # return ["http/1.1", "h2", ""]
        return []
