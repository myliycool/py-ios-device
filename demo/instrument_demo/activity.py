"""
获取单个应用 activity数据
"""
import time
import os
import sys

from servers.DTXSever import pre_call

sys.path.append(os.getcwd())
from servers.Instrument import  InstrumentServer
from util import logging

log = logging.getLogger(__name__)


def activity(rpc, pid):
    def on_callback_message(res):
        print(f"[ACTIVITY] {res.parsed}", )
        print("\n")

    pre_call(rpc)
    rpc.register_channel_callback("com.apple.instruments.server.services.activity", on_callback_message)
    # rpc.register_channel_callback("com.apple.instruments.server.services.activity", callback)
    var = rpc.call("com.apple.instruments.server.services.activity", "startSamplingWithPid:", pid).parsed
    log.debug(f"start {var}")

    time.sleep(10)
    var = rpc.call("com.apple.instruments.server.services.activity", "stopSampling").parsed
    log.debug(f"stop {var}")
    rpc.stop()


if __name__ == '__main__':
    rpc = InstrumentServer().init()
    activity(rpc, 31630)
    rpc.deinit()
