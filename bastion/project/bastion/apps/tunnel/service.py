from bastion.apps.tunnel.schema import Tunnel
from bastion.apps.tunnel.util import list_open_tunnel


class TunnelService(object):
    def __init__(self):
        pass

    def list_tunnels(self) -> list[Tunnel]:
        return list_open_tunnel()
