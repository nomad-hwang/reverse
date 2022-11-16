import abc
import ssl


class BaseResolver(abc.ABC):
    """Interface for resolver"""

    async def resolve(self, sslobj: ssl.SSLObject) -> tuple[str, int]:
        """Resolve SNI and ALPN based on the request headers and return the upstream address"""
        return await self._resolve(get_sni(sslobj), get_alpn(sslobj))

    @abc.abstractmethod
    async def _resolve(self, sni: str, alpn: str) -> tuple[str, int]:
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
    return sslobj.context.get_sni(sslobj)


def get_alpn(sslobj: ssl.SSLObject) -> str:
    """Get ALPN value from SSLObject"""
    return sslobj.selected_alpn_protocol()
