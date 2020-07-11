import argparse
import sys
from pkscan_print_server.server import start

class PkscanServer(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='PK Scan Server',
            usage='''pkscan-server <command> [<args>]

The allowed commands are:
   start      Start the server
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def start(self):
        parser = argparse.ArgumentParser(
            description="Start histor server for prntouts")
        parser.add_argument("--filename",
                            type=str,
                            help="Give the filename of the file where all history need to be stored")
        parser.add_argument("--counter",
                            type=int,
                            help="Give the counter for the machine")
        args = parser.parse_args(sys.argv[2:])
        start(args.filename, args.counter)