from pydantic import BaseModel


class LinuxConfig(BaseModel):
    group: str = "tunnel_users_group"
    shell: str = "/bin/false"
