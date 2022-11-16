import asyncio
import ssl
from typing import Set

from core.proxy_server.forwarder import ForwarderMixin
from core.proxy_server.util.resolver import BaseResolver
from core.proxy_server.util.ssl import SSLContextBuilder


class ForwardServer(ForwarderMixin):
    """Forward traffic to upstream server"""

    def __init__(
        self, host: str, port: int, sslctx: ssl.SSLContext, resolver: BaseResolver
    ) -> None:
        self._host = host
        self._port = port
        self._sslctx = sslctx
        self._resolver = resolver

        self._session: Set[asyncio.Task] = set()

    async def serve(self) -> None:
        self._logger.info(f"Starting server on {self._host}:{self._port}")

        try:
            _server = await asyncio.start_server(
                self._connected_cb, host=self._host, port=self._port, ssl=self._sslctx
            )
            await _server.serve_forever()
        except asyncio.CancelledError:
            pass

        self._logger.info(f"Stopping server on {self._host}:{self._port}")
        for s in self._session:
            s.cancel()
        if self._session:
            await asyncio.wait(self._session)

    async def _connected_cb(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        """Client connected callback. resolve sni and alpn and forward traffic"""
        sess = asyncio.create_task(self._forward(self._resolver, reader, writer))
        sess.add_done_callback(lambda _: self._session.discard(sess))
        self._session.add(sess)

    @property
    def resolver(self) -> BaseResolver:
        return self._resolver


def make_forward_server(
    host: str, port: int, cert_path: str, key_path: str, resolver: BaseResolver
) -> ForwardServer:
    """Create a forward server"""
    sslctx = (
        SSLContextBuilder()
        .with_cert_chain(cert_path, key_path)
        .with_accepted_protocols(resolver.accepted_protocols)
        .build()
    )
    return ForwardServer(host, port, sslctx, resolver)
