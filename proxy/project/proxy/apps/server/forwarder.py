import asyncio
import logging
import weakref

from core.proxy_server.util.resolver import BaseResolver
from core.proxy_server.util.ssl import SSLContextBuilder


class ForwarderMixin(object):

    _logger = logging.getLogger(__name__)

    async def _forward(
        self,
        resolver: BaseResolver,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ):
        try:
            up_host, up_port = await resolver.resolve(
                writer.get_extra_info("ssl_object")
            )

            self._logger.debug(
                f"[{id(writer)} Fowarding from {writer.get_extra_info('peername')} to ({up_host}, {up_port})"
            )

            try:
                up_reader, up_writer = await asyncio.open_connection(up_host, up_port)
            except Exception as e:
                self._logger.error(f"[{id(writer)} Failed to connect to upstream: {e}")
                writer.transport.abort()
                await writer.wait_closed()
                return

            up = asyncio.create_task(self._forward_stream(reader, up_writer))
            dn = asyncio.create_task(self._forward_stream(up_reader, writer))
            await asyncio.wait([up, dn])
        except (asyncio.CancelledError, ConnectionResetError):
            up.cancel()
            dn.cancel()
            await asyncio.wait([up, dn])
        finally:
            self._logger.debug(f"[{id(writer)} Closed forwarding")

    async def _forward_stream(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        """Forward traffic from reader to writer"""
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except (asyncio.CancelledError, ConnectionResetError):
            writer.close()
            await writer.wait_closed()
            raise
