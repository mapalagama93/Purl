import os
import argparse

class Args:

    root = os.getcwd()
    env = []
    files = []
    is_curl = False
    is_init = False

    def parse(self):
        __parser = argparse.ArgumentParser(prog='purl')
        __parser.add_argument('-i', '--init', action='store_true', help='initialize folders and file structure at current directory. use -e flag to specify env files to be generated.') 
        __parser.add_argument('-c', '--curl', action='store_true', help='generate curl command instead of sending request.') 
        __parser.add_argument('-e', '--env', nargs='*', help='specify list of env to apply.') 
        __parser.add_argument('-f', '--file', nargs='*', help='specify list of actions to be performed.') 
        __parser = __parser.parse_args()
        self.env = __parser.env if __parser.env != None else []
        self.files = __parser.file if __parser.file != None else []
        self.is_curl = __parser.curl
        self.is_init = __parser.init

args = Args()