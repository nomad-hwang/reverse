from pydantic import BaseModel


class Tunnel(BaseModel):
    name: str
    port: int
    protocol: str
