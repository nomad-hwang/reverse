from dataclasses import dataclass
from typing import Any


@dataclass
class Config(object):
    HOST: str = ""
    PORT: int = 443

    BASE_DOMAIN: str = "dev.dawoon.com"
    CERT_PATH = f"/etc/letsencrypt/live/{BASE_DOMAIN}/fullchain.pem"
    KEY_PATH = f"/etc/letsencrypt/live/{BASE_DOMAIN}/privkey.pem"

    BASTION: dict[str, Any] = {
        "bastion": {
            "host": "bastion",
            "port": 8080,
        },
    }

    BASTION_TUNNEL_HOST: str = "bastion"


settings = Config()

__all__ = ["settings"]
