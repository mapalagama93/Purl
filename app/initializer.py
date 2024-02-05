from app.args import args
from termcolor import cprint
from pathlib import Path

__sample_request = """
Method: POST
Endpoint: ${server}/api/json

JsonBody: |
  {
    "sample key" : "sample json value"
  }

Headers:
  Authorization: Basic c2RmZzIzNDEyM3JlZnNkc2Rm

Captures:
  title: "@body jsonpath $.glossary.title"
  date: "@headers Date"

Asserts:
  "status code is 503" : "@status |==| 429"
  "date header" : "@headers Date"
  "check value not null" : "@body jsonpath $.glossary.title"
  "check value not equal" : "@body jsonpath $.glossary.title |==| example glossary"
"""

class Initializer:

    __files = ['/configs/config.properties', '/configs/store.properties', '/sample.yaml']
    __dirs = ['/configs']
    __file_content = {
            '/sample.yaml' : globals()['__sample_request']
    }

    def init(self):
        self.__files = self.__files + ['/configs/' + x + '.properties' for x in args.env]
        self.create_dirs()
        self.create_files()
        self.write_to_files()

    def create_dirs(self):
        for d in self.__dirs:
            dpath = args.root + d;
            Path(dpath).mkdir(exist_ok=True)
            cprint('Create folder ' + dpath, 'green')

    def create_files(self):
        for f in self.__files:
            fpath = args.root + f
            Path(fpath).touch(exist_ok=True)
            cprint('Create file ' + fpath, 'green')

    def write_to_files(self):
        for f, content in self.__file_content.items():
            with open(args.root + f, '+a') as file :
                file.write(content)