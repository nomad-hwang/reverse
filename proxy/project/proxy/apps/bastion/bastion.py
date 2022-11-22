import asyncio
import aiohttp
from cache import AsyncTTL
from proxy.apps.bastion.schema import Device, Tunnel
from proxy.config import config

# OPENAPI3 = {"openapi":"3.0.2","info":{"title":"FastAPI","version":"0.1.0"},"paths":{"/api/v1/device":{"get":{"tags":["device"],"summary":"Get Devices","operationId":"get_devices_api_v1_device_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"title":"Response Get Devices Api V1 Device Get","type":"array","items":{"$ref":"#/components/schemas/Device"}}}}}}},"post":{"tags":["device"],"summary":"Create Device","operationId":"create_device_api_v1_device_post","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/DeviceCreate"}}},"required":true},"responses":{"201":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/Device"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/v1/tunnel":{"get":{"tags":["tunnel"],"summary":"Get Open Tunnels","operationId":"get_open_tunnels_api_v1_tunnel_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"title":"Response Get Open Tunnels Api V1 Tunnel Get","type":"array","items":{"$ref":"#/components/schemas/Tunnel"}}}}}}}},"/":{"get":{"summary":"Root","operationId":"root__get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}}}}}},"components":{"schemas":{"Device":{"title":"Device","required":["name","ssh_key","active"],"type":"object","properties":{"name":{"title":"Name","type":"string"},"ssh_key":{"title":"Ssh Key","type":"string"},"alias":{"title":"Alias","type":"string"},"active":{"title":"Active","type":"boolean"}}},"DeviceCreate":{"title":"DeviceCreate","required":["name","ssh_key"],"type":"object","properties":{"name":{"title":"Name","type":"string"},"ssh_key":{"title":"Ssh Key","type":"string"}}},"HTTPValidationError":{"title":"HTTPValidationError","type":"object","properties":{"detail":{"title":"Detail","type":"array","items":{"$ref":"#/components/schemas/ValidationError"}}}},"Tunnel":{"title":"Tunnel","required":["user","port"],"type":"object","properties":{"user":{"title":"User","type":"string"},"port":{"title":"Port","type":"integer"}}},"ValidationError":{"title":"ValidationError","required":["loc","msg","type"],"type":"object","properties":{"loc":{"title":"Location","type":"array","items":{"anyOf":[{"type":"string"},{"type":"integer"}]}},"msg":{"title":"Message","type":"string"},"type":{"title":"Error Type","type":"string"}}}}}}

URL = f"http://{config.BASTION_API_HOST}:{config.BASTION_API_PORT}"


@AsyncTTL(time_to_live=2)
async def get_port(name: str, protocol: str = "tcp") -> int:
    for tunnel in await get_open_tunnels():
        if tunnel.name == name and tunnel.protocol == protocol:
            return tunnel.port
    raise ValueError(f"Device '{name}' not found or not open")


@AsyncTTL(time_to_live=5)
async def get_open_tunnels() -> list[Tunnel]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}/api/v1/tunnel") as resp:
            return [Tunnel(**tunnel) for tunnel in await resp.json()]


async def get_all_device() -> list[Device]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}/api/v1/device") as resp:
            return await resp.json()
