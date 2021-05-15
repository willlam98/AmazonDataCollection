import argparse

class CLIParser():

    def __init__(self):
        self.cli_parser = argparse.ArgumentParser(
            description='Download product information from Amazon given .json file'
        )
        self.cli_parser.add_argument('-f', dest='file', help='Target .json file')
        self.cli_parser.add_argument('-obj', dest='object', help='Specify object name')
        self.cli_parser.add_argument('-img', dest='image', help='Download image')

    def parse(self):
        args = self.cli_parser.parse_args()
        return args.file, args.object, args.image