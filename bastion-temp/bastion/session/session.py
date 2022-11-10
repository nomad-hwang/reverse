import weakref


class Session(object):
    session = weakref.WeakValueDictionary()

    def __init__(self, session_id):
        self.session_id = session_id
        self.session[session_id] = self

    def __del__(self):
        del self.session[self.session_id]
