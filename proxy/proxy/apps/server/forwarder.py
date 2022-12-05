import asyncio
import logging
import weakref

from proxy.apps.resolver.resolver import BaseResolver


class ForwarderMixin(object):

    _logger = logging.getLogger(__name__)

    _active_forwarders = weakref.WeakSet()

    async def _forward(
        self,
        resolver: BaseResolver,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ):
        try:
            try:
                up_reader, up_writer = await resolver.connect_upstream(
                    writer.get_extra_info("ssl_object")
                )
            except Exception as e:
                self._logger.error(f"[{id(writer)}] Failed to connect to upstream: {e}")
                writer.transport.abort()
                await writer.wait_closed()
                return

            up = asyncio.create_task(self._forward_stream(reader, up_writer))
            dn = asyncio.create_task(self._forward_stream(up_reader, writer))
            self._active_forwarders.add(up)

            await asyncio.wait([up, dn])  # TODO how about asyncio.gather?
        except (asyncio.CancelledError):
            up.cancel()
            dn.cancel()
            await asyncio.wait([up, dn])
        finally:
            self._logger.info(
                f"[{id(writer)}] Forwarding closed. Current active connection: {len(self._active_forwarders)}"
            )

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
        except (asyncio.CancelledError, ConnectionResetError) as e:
            if e is ConnectionResetError:
                self._logger.info(f"[{id(writer)}] Connection reset by peer")
            writer.close()
            await writer.wait_closed()
