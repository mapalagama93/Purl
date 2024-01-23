from jproperties import Properties
from pathlib import Path
import os
from termcolor import cprint

class Vars:
    __configs = Properties()
    __store = Properties()
    __context = Properties()

    __env_files = []
    __is_store_file_exists = True

    def init(self, args):
        self.__config_file = args.root + '/configs/config.properties'
        self.__store_file = args.root + '/configs/store.properties'
        self.__env_files = [args.root + '/configs/' + file + '.properties' for file in args.env]
        self.__load_config()
        self.__load_store()
        self.__load_envs()

    def get(self, key, default_alue = ''):
        if key in self.__context:
            return self.__context[key].data

        if key in self.__store:
            return self.__store[key].data
        
        if key in self.__configs:
            return self.__configs[key].data
        
        return default_alue

    def set(self, key, value):
        self.__store[key] = value
        self.__sync_store()
    
    def get_all(self):
        all = Properties()
        all.update(self.__configs)
        all.update(self.__store)
        all.update(self.__context)
        return all

    def __load_config(self):
        if os.path.exists(self.__config_file) == False:
             return
        with open(self.__config_file, 'rb') as file:
            self.__configs.load(file, 'utf-8')

    def __load_store(self):
        if os.path.exists(self.__store_file) == False:
             self.__is_store_file_exists = False
             return
        with open(self.__store_file, 'rb') as file:
            self.__store.load(file, 'utf-8')

    def __load_envs(self):
        for fpath in self.__env_files:
            if(os.path.exists(fpath) == False):
                cprint(fpath + ' file does not exists.', 'yellow')
                continue
            with open(fpath, 'rb') as file:
                self.__configs.load(file, 'utf-8')

    def __sync_store(self):
        if not self.__is_store_file_exists:
            return
        with open(self.__store_file, 'wb') as file:
            self.__store.store(file, encoding='utf-8')
    
    def set_context(self, key, value):
        self.__context[key] = value

vars = Vars()