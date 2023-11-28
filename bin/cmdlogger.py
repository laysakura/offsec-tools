import logging


class CmdLogger:
    def __init__(self, level=logging.INFO):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        # fmt_info_yellow = logging.Formatter('\033[33m[*] Running: %(message)s\033[0m')
        stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(fmt_info_yellow)
        logger.addHandler(stream_handler)

        self.logger = logger
        self.level = level

    def running(self, cmdline):
        self.logger.info(self._yellow(f"[*] Running: {cmdline}"))

    def progress(self, msg):
        self.logger.info(self._blue(f"[o] {msg}"))

    def finish(self, msg):
        self.logger.info(self._green(f"[0] Success: {msg}"))

    def abort(self, msg):
        self.logger.info(self.red(f"[x] Aborted: {msg}"))

    def _yellow(self, s):
        return "\033[33m%s\033[0m" % s

    def _blue(self, s):
        return "\033[34m%s\033[0m" % s

    def _green(self, s):
        return "\033[32m%s\033[0m" % s
    
    def red(self, s):
        return "\033[31m%s\033[0m" % s