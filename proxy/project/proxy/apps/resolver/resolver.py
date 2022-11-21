import abc
import ssl
from asyncio import StreamReader, StreamWriter

from proxy.apps.server.util.ssl import SNIStore


class BaseResolver(abc.ABC):
    """Interface for resolver"""

    async def connect_upstream(
        self, sslobj: ssl.SSLObject
    ) -> tuple[StreamReader, StreamWriter]:
        """Resolve SNI and ALPN based on the request headers and return the upstream address"""
        return await self._routed_connection(get_sni(sslobj), get_alpn(sslobj))

    @abc.abstractmethod
    async def _routed_connection(
        self, sni: str, alpn: str
    ) -> tuple[StreamReader, StreamWriter]:
        """Implement this method to resolve SNI and ALPN and return the upstream address"""
        pass

    @abc.abstractproperty
    def accepted_protocols(self) -> list[str]:
        """Return the accepted protocols.
        Without proper setup, alpn appears to be None.
        """
        pass


def get_sni(sslobj: ssl.SSLObject) -> str:
    """Get SNI value from SSLObject"""
    context: SNIStore = sslobj.context
    return context.get_sni(sslobj)


def get_alpn(sslobj: ssl.SSLObject) -> str:
    """Get ALPN value from SSLObject"""
    return sslobj.selected_alpn_protocol()
