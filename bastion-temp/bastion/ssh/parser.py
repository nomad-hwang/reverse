from enum import Enum


class SshEventType(str, Enum):
    """SSH event types"""

    AUTH = "auth"
    COMMAND = "command"
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    FORWARD = "forward"
    SESSION = "session"
    TUNNEL = "tunnel"

    def __str__(self):
        return str(self.value)


class SshEvent(object):
    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.event_data = event_data

    def __str__(self):
        return f"{self.event_type}: {self.event_data}"
