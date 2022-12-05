import ssl
import weakref


class SNIStore(ssl.SSLContext):
    """SSLContextContainer to store the SNI value"""

    @classmethod
    def create_from(cls, sslctx: ssl.SSLContext) -> "SNIStore":
        self = cls(sslctx.protocol)
        self.__dict__.update(sslctx.__dict__)
        self._store = weakref.WeakKeyDictionary()
        self.set_servername_callback(self._cb)
        return self

    def _cb(self, sslobj, servername, sslctx):
        self._store.update({sslobj: servername})  # Keep SNI

    def get_sni(self, sslobj) -> str:
        return self._store.get(sslobj)


class SSLContextBuilder(object):
    """SSLContextBuilder to build SSLContext"""

    def __init__(self, purpose: ssl.Purpose = ssl.Purpose.CLIENT_AUTH) -> None:
        self._sslctx = SNIStore.create_from(ssl.create_default_context(purpose))

    def with_cert_chain(
        self, certfile: str, keyfile: str = None
    ) -> "SSLContextBuilder":
        self._sslctx.load_cert_chain(certfile, keyfile)
        return self

    def with_accepted_protocols(self, protocols: list) -> "SSLContextBuilder":
        self._sslctx.set_alpn_protocols(protocols)
        return self

    def build(self) -> SNIStore:
        return self._sslctx
