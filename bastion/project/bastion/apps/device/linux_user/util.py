import grp
import os
import pwd

from bastion.apps.device.linux_user.exceptions import (
    UserBaseError,
    UserExists,
    UserNotFound,
)


def adduser(username: str, group: str, shell: str) -> None:
    if user(username):
        raise UserExists

    cmd(f"useradd -m {username} -s /bin/true")
    cmd(f"passwd -d {username}")  # Remove password


def register_ssh_key(username: str, group: str, key: str) -> None:
    user(username, raise_on_not_found=True)
    os.makedirs(f"/home/{username}/.ssh", exist_ok=True)
    cmd(f"echo '{key}' > /home/{username}/.ssh/authorized_keys")


def get_ssh_key(username: str) -> str:
    user(username, raise_on_not_found=True)
    with open(f"/home/{username}/.ssh/authorized_keys", "r") as f:
        return f.read().strip()


def create_group(groupname: str) -> None:
    # try:
    #     grp.getgrnam(groupname)  # check if group exists
    # except KeyError:
    #     if os.system(f"addgroup {groupname}"):
    #         raise UserBaseError
    pass


def user(username: str, raise_on_not_found=False) -> pwd.struct_passwd | None:
    try:
        return pwd.getpwnam(username)
    except KeyError:
        if raise_on_not_found:
            raise UserNotFound


def cmd(cmd: str) -> None:
    if os.system(cmd):
        raise UserBaseError
