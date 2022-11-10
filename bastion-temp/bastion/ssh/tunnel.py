from dataclasses import dataclass


@dataclass
class Connection(object):
    pid: int
    user: str
    host: str
    port: int
    status: str
    protocol: str
    laddr: str
    raddr: str
    lport: int
    rport: int
    family: int
    type: int


def get_ssh_connection_info(connected_port):
    """
    COMMAND  PID     USER   FD   TYPE    DEVICE SIZE/OFF NODE NAME
    sshd.pam 155 testuser    3u  IPv4 128328282      0t0  TCP *:2222 (LISTEN)
    sshd.pam 155 testuser    4u  IPv6 128328283      0t0  TCP *:2222 (LISTEN)
    sshd.pam 183 testuser    4u  IPv4 128336797      0t0  TCP 192.168.48.2:2222->192.168.48.1:59668 (ESTABLISHED)
    sshd.pam 185 testuser    4u  IPv4 128336797      0t0  TCP 192.168.48.2:2222->192.168.48.1:59668 (ESTABLISHED)
    sshd.pam 963 testuser    4u  IPv4 129135639      0t0  TCP 192.168.48.2:2222->192.168.48.1:48828 (ESTABLISHED)
    sshd.pam 965 testuser    4u  IPv4 129135639      0t0  TCP 192.168.48.2:2222->192.168.48.1:48828 (ESTABLISHED)
    sshd.pam 965 testuser    5u  IPv4 129134078      0t0  TCP *:42199 (LISTEN)
    sshd.pam 965 testuser    7u  IPv6 129134079      0t0  TCP *:42199 (LISTEN)
    """
    tunnels = []
    for conn in psutil.net_connections(kind="tcp"):
        if conn.status == "LISTEN":
            if conn.laddr.port == 2222:
                tunnels.append(conn)
    return tunnels
