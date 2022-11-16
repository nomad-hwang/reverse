from pydantic import BaseModel


class Tunnel(BaseModel):
    user: str
    port: int
