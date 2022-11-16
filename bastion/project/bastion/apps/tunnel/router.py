from bastion.apps.tunnel.schema import Tunnel
from bastion.apps.tunnel.util import list_open_tunnel
from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("", response_model=list[Tunnel])
def get_open_tunnels():
    return list_open_tunnel()
