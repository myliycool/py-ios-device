import os
import sys

sys.path.append(os.getcwd())
from threading import Event
from servers.Instrument import InstrumentServer
from util.dtxlib import auxiliary_to_pyobject
from util import logging

log = logging.getLogger(__name__)


def channels(rpc):
    done = Event()

    def _notifyOfPublishedCapabilities(res):
        done.set()
        log.debug("Published capabilities:")
        for k, v in auxiliary_to_pyobject(res.raw._auxiliaries[0]).items():
            print(k, v)

    rpc.register_callback("_notifyOfPublishedCapabilities:", _notifyOfPublishedCapabilities)
    rpc.start()
    if not done.wait(5):
        log.debug("[WARN] timeout waiting capabilities")
    rpc.stop()


if __name__ == '__main__':
    rpc = InstrumentServer().init()
    channels(rpc)
    rpc.deinit()
