import aiohttp
from cache import AsyncTTL
from proxy.apps.bastion.schema import Device, Tunnel
from proxy.config import settings

BASTION_URLS: list[str] = [
    f"http://{hostname}:{port}" for hostname, port in settings.BASTION.items()
]


@AsyncTTL(time_to_live=2)
async def get_port(name: str, protocol: str = "tcp") -> int:
    for tunnel in await get_open_tunnels():
        if tunnel.name == name and tunnel.protocol == protocol:
            return tunnel.port
    raise ValueError(f"Device '{name}' not found or not open")


@AsyncTTL(time_to_live=5)
async def get_open_tunnels() -> list[Tunnel]:
    async with aiohttp.ClientSession() as session:
        results = []
        for url in BASTION_URLS:
            try:
                async with session.get(f"{url}/api/v1/tunnel") as resp:
                    results.extend(
                        [
                            Tunnel(**tunnel, protocol="tcp")
                            for tunnel in await resp.json()
                        ]
                    )
            except Exception:
                pass
        return results


async def get_all_device() -> list[Device]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}/api/v1/device") as resp:
            return await resp.json()
