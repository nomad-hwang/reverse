import subprocess

from bastion.apps.tunnel.schema import Tunnel


def list_open_tunnel() -> list[Tunnel]:
    proc = subprocess.Popen(
        ["netstat", "-tle"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    lines = out.decode().splitlines()
    lines = lines[2:]

    tunnels = []
    for line in lines:
        line = line.split()
        port = line[3].split(":")[-1]
        user = line[6]
        if user != "0" and user != "root":
            tunnels.append(Tunnel(user=user, port=int(port)))
    return tunnels
