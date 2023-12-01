import argparse


class CmdArgs:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Nmap Scanner Made Easy")
        parser.add_argument("ip", help="IP address to scan")
        parser.add_argument("-f", "--full", action="store_true", help="Scan all ports")
        parser.add_argument(
            "-d", "--dry-run", action="store_true", help="Perform a dry run"
        )
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
        parser.add_argument(
            "nmapopts", nargs="*", help="Optional arguments to pass to nmap"
        )
        args = parser.parse_args()

        self.ip = args.ip
        self.full = args.full
        self.dry_run = args.dry_run
        self.verbose = args.verbose
        self.nmapopts = args.nmapopts
