import os
import pyinotify
import logging
from datetime import datetime
import time

class EventProcessor(pyinotify.ProcessEvent):

    def __init__(self, pevent=None, eventq = "test", **kargs):
        super().__init__(pevent=pevent, **kargs)
        self.eventq = eventq
        pass

    _methods = ["IN_CREATE",
                "IN_OPEN",
                "IN_ACCESS",
                "IN_ATTRIB",
                "IN_CLOSE_NOWRITE",
                "IN_CLOSE_WRITE",
                "IN_DELETE",
                "IN_DELETE_SELF",
                "IN_IGNORED",
                "IN_MODIFY",
                "IN_MOVE_SELF",
                "IN_MOVED_FROM",
                "IN_MOVED_TO",
                "IN_Q_OVERFLOW",
                "IN_UNMOUNT",
                "default"]

def process_generator(cls, method):
    def _method_name(self, event):
        msgdict = {"datetime":str(datetime.now()), "time":time.time(),"method": method, "path": event.pathname, "event": event.maskname}
        msg = "Method name: process_{}(), Path name: {}, Event Name: {}".format(method, event.pathname, event.maskname)
        
        logging.warning(msg)
        self.eventq.put(msgdict, False)

    
    _method_name.__name__ = "process_{}".format(method)
    setattr(cls, _method_name.__name__, _method_name)

for method in EventProcessor._methods:
    process_generator(EventProcessor, method)
