from dataclasses import dataclass


@dataclass
class Tunnel(object):
    name: str
    port: int
    protocol: str


@dataclass
class Device(object):
    name: str
    ssh_key: str
    alias: str
    active: bool
