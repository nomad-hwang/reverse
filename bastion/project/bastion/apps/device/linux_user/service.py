import os

from bastion.apps.device.linux_user.config import LinuxConfig
from bastion.apps.device.linux_user.exceptions import (
    UserExpired,
    UserLocked,
    UserNotFound,
)
from bastion.apps.device.linux_user.util import (
    adduser,
    create_group,
    get_ssh_key,
    register_ssh_key,
    user,
)

shadow_error_map = {
    UserNotFound: ["NP", None, "!"],
    UserLocked: ["LK", "*"],
    UserExpired: ["!!"],
}


class LinuxUserService(object):
    def __init__(self, options=LinuxConfig()):
        self._opts = options

        if os.geteuid() != 0:
            raise PermissionError("requires root previledge")
        create_group(self._opts.group)

    def create(self, username: str, ssh_key: str, active: bool = False) -> None:
        adduser(username, self._opts.group, self._opts.shell)
        register_ssh_key(username, self._opts.group, ssh_key)

    def update_ssh_key(self, username: str, ssh_key: str) -> None:
        register_ssh_key(username, self._opts.group, ssh_key)

    def get_ssh_key(self, username: str) -> str:
        return get_ssh_key(username)

    def active(self, username: str) -> bool:
        return True  # TODO: implement

    def update_active(self, username: str, active: bool) -> None:
        pass  # TODO: implement

    def user_exists(self, username: str) -> bool:
        return user(username) != None
