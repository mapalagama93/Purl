import os
import argparse
import logging
import re

class Args:

    root = os.getcwd()
    env = []
    files = []
    is_curl = False
    is_init = False
    is_debug = False
    options = {}
    variables = {}
    collection = None
    

    def parse(self):
        __parser = argparse.ArgumentParser(prog='purl')
        __parser.add_argument('-i', '--init', action='store_true', help='initialize folders and file structure at current directory. use -e flag to specify env files to be generated.') 
        __parser.add_argument('-c', '--curl', action='store_true', help='generate curl command instead of sending request.') 
        __parser.add_argument('-d', '--debug', action='store_true', help='output debug logs') 
        __parser.add_argument('-e', '--env', nargs='*', help='specify list of env to apply.') 
        __parser.add_argument('-f', '--files', nargs='*', help='specify list of actions to be performed.')
        __parser.add_argument('-o', '--options',nargs='*', help='purl options -o insecure=false timeout=90') 
        __parser.add_argument('-v', '--vars',nargs='*', help='override vars eg : -v userId=123 userEmail=example@gmail.com') 
        __parser.add_argument('-k', '--collection',type=str, help='run collection file.') 

        __parser = __parser.parse_args()
        self.env = __parser.env if __parser.env != None else []
        self.files = __parser.files if __parser.files != None else []
        self.is_curl = __parser.curl
        self.is_init = __parser.init
        self.is_debug = __parser.debug
        self.options = self.__parse_key_value(__parser.options if __parser.options != None else [])
        self.variables =  self.__parse_key_value( __parser.vars if __parser.vars != None else [])


    def __parse_key_value(self, arr):
        d = {}
        for v in arr:
            s = re.split(r'(?<!\\)=', v)
            if len(s) != 2 :
                raise Exception('Invalid variable ' + v)
            d[s[0]] = s[1]
            print(v)
        return d

args = Args()