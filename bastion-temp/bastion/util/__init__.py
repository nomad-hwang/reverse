from enum import Enum


class SshEventDispatcher(object):
    def __init__(self, session):
        self.session = session

    def __call__(self, event):
        self.session.event(event)
