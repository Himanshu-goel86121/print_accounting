import argparse
import sys
from pkscan_print_server.server import start
from pkscan_print_server.utils import Convert

class PkscanServer(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='PK Scan Server',
            usage='''pk <command> [<args>]

The allowed commands are:
   start      Start the server
   convert    Convert log files to different formats
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
            description="Start history server for prntouts")
        parser.add_argument("--filename",
                            type=str,
                            help="Give the filename of the file where all history need to be stored",
                            required=False,
                            default="D://print_logs/logs.csv")
        parser.add_argument("--backup_filename",
                            type=str,
                            help="Give the filename of backup",
                            required=False,
                            default="G://print_logs_backup/logs.csv")
        args = parser.parse_args(sys.argv[2:])
        start(args.filename, args.backup_filename)

    def convert(self):
        parser = argparse.ArgumentParser(
            description="Start history server for prntouts")
        parser.add_argument("--filename",
                            type=str,
                            help="Give the filename of the file where all history need to be stored",
                            required=False,
                            default="D://print_logs/logs.csv")
        parser.add_argument("--to",
                            type=str,
                            help="Choose the format to convert the file",
                            required=True,
                            choices=["paper",
                                     "counter_daily",
                                     "paper_daily",
                                     "paper_monthly"])
        args = parser.parse_args(sys.argv[2:])
        convert_obj = Convert(args.filename)
        getattr(convert_obj, args.to)()
