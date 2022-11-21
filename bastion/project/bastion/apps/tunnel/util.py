import subprocess

from bastion.apps.tunnel.schema import Tunnel

""" 
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode
tcp        0      0 0.0.0.0:ssh             0.0.0.0:*               LISTEN      root       72940
tcp        0      0 0.0.0.0:42233           0.0.0.0:*               LISTEN      bf66355f399f4e15a165f080d97c082b 74131
tcp        0      0 localhost:32875         0.0.0.0:*               LISTEN      root       72582
tcp        0      0 0.0.0.0:http-alt        0.0.0.0:*               LISTEN      root       73289
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN      root       72942
tcp6       0      0 [::]:42233              [::]:*                  LISTEN      bf66355f399f4e15a165f080d97c082b 74132
"""

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
        name = line[6]
        if name != "0" and name != "root":
            tunnels.append(Tunnel(name=name, port=int(port), protocol=line[0]))
    return tunnels
