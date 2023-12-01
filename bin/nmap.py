import subprocess
import os
import sys
import datetime


class Nmap:
    def __init__(self, logger, ip, dry_run=False, full_ports=False, nmapopts=[]):
        self.logger = logger
        self.ip = ip
        self.dry_run = dry_run
        self.full_ports = full_ports
        self.nmapopts = nmapopts

        self.open_ports = set()

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.dirname = f"nmap-mania-{timestamp}"

        os.mkdir(self.dirname)
        self.logger.progress(f"Log directory: {self.dirname}")

    def scan_ports(self):
        self._run_nmap_cmd(["-sS", "-T4", "-F"])
        if self.full_ports:
            self._run_nmap_cmd(["-sS", "-p-"])

    def scan_versions(self):
        self._scan_open_ports(["-sV"])

    def scan_vuln(self):
        self._scan_open_ports(["--script", "vuln"])

    def log_ports(self):
        if self.dry_run:
            pass
        else:
            self.logger.finish("Print open ports so far:")
            sorted_ports = sorted(self.open_ports)
            print(",".join([str(p) for p in sorted_ports]))

    def _run_nmap_cmd(self, args_arr):
        args = self.nmapopts + args_arr
        args_space_separated = " ".join(args)
        args_underscore_separated = "_".join(args)
        log_filename = f"{self.dirname}/{args_underscore_separated}.log"

        self.logger.running(f"nmap -oN {log_filename} {args_space_separated} {self.ip}")

        if not self.dry_run:
            ret = subprocess.run(
                ["nmap", "-oN", log_filename] + args + [self.ip],
                # capture nmap stdout
                stdout=subprocess.PIPE,
            )
            # nmap stdout to stderr
            self.logger.cmd_output(ret.stdout.decode("utf-8"))

            if ret.returncode != 0:
                self.logger.abort("")
                raise Exception("nmap command failed")
            else:
                self.logger.progress(f"Dumped: {log_filename}")
                self._update_open_ports(log_filename)

    def _scan_open_ports(self, args_arr):
        if self.open_ports:
            self._run_nmap_cmd(args_arr + [f"-p{self._open_ports_str()}"])
        else:
            self.logger.abort("No open ports to scan deeper")

    def _open_ports_str(self):
        sorted_ports = sorted(self.open_ports)
        return ",".join([str(p) for p in sorted_ports])

    def _update_open_ports(self, log_filename):
        with open(log_filename, "r") as f:
            for line in f.readlines():
                if "/tcp" in line and "open" in line:
                    port = int(line.split("/")[0])
                    self.open_ports.add(port)
