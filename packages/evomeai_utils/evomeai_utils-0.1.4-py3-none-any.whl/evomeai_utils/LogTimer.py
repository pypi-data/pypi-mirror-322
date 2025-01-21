import json
import logging
import time
import sys

log = logging.getLogger('LogTimer')

class LogTimer:
    timers = []
    def __init__(self, name):
        #获取当前函数调用堆栈深度
        track = sys._getframe(1)
        layer = 0
        while track.f_globals.get('__name__') != '__main__':
            log.debug(f"track.f_globals.get('__name__'): {track.f_globals.get('__name__')}")
            track = track.f_back
            if track is None:
                break
            layer += 1

        self.name = '  ' * layer + name
        self.start_time = time.time()
        self.elapsed_time = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed_time = time.time() - self.start_time
        LogTimer.timers.append(self)
        log.debug(f"{self.name} time: {self.elapsed_time*1000:.3f} ms")

    @staticmethod
    def output():
        res = {}
        for timer in LogTimer.timers:
            res[timer.name] = f"{timer.elapsed_time:.3f}s"
        log.info("Total Time Cost: " + json.dumps(res, indent=2))

        LogTimer.timers = []
        return res