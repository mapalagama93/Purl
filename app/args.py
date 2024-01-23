import os
import argparse

__parser = argparse.ArgumentParser(prog='purl')
__parser.add_argument('-i', '--init', action='store_true', help='initialize folders and file structure at current directory. use -e flag to specify env files to be generated.') 
__parser.add_argument('-c', '--curl', action='store_true', help='generate curl command instead of sending request.') 
__parser.add_argument('-e', '--env', nargs='*', help='specify list of env to apply.') 
__parser.add_argument('-f', '--file', nargs='*', help='specify list of actions to be performed.') 
__parser = __parser.parse_args()

root = os.getcwd()
env = __parser.env if __parser.env != None else []
actions = __parser.file if __parser.file != None else []
is_curl = __parser.curl
is_init = __parser.init