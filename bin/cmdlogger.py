import logging


class CmdLogger:
    def __init__(self, verbose=False):
        logger = logging.getLogger(__name__)
        if verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)

        self.logger = logger

    def running(self, cmdline):
        self.logger.info(self._yellow(f"[*] Running: {cmdline}"))

    def progress(self, msg):
        self.logger.info(self._blue(f"[o] {msg}"))

    def finish(self, msg):
        self.logger.info(self._green(f"[0] Success: {msg}"))

    def abort(self, msg):
        self.logger.info(self.red(f"[x] Aborted: {msg}"))

    def cmd_output(self, cmdout):
        self.logger.debug(cmdout)

    def _yellow(self, s):
        return "\033[33m%s\033[0m" % s

    def _blue(self, s):
        return "\033[34m%s\033[0m" % s

    def _green(self, s):
        return "\033[32m%s\033[0m" % s
    
    def red(self, s):
        return "\033[31m%s\033[0m" % s
