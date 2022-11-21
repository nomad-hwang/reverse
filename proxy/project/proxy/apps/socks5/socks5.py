import asyncio
from python_socks.async_.asyncio import Proxy

async def create_connection(socks_host, socks_port, host, port):
    proxy = Proxy.from_url(f"socks5://{socks_host}:{socks_port}")
    
    sock = await proxy.connect(dest_host=host, dest_port=port)
    
    return await asyncio.open_connection(
        host=None,
        port=None,
        sock=sock,
    )
