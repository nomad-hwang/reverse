from dataclasses import dataclass


@dataclass
class Config(object):
    BASTION_API_HOST: str = "bastion"
    BASTION_API_PORT: int = 8080

    BASTION_TUNNEL_HOST: str = "bastion"


config = Config()

__all__ = ["config"]
