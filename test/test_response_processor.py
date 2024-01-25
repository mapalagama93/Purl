from app.vars import vars 
import unittest
import os
from app.args import args
from app.pfile import PFile
from app.core.response_processor import ResponseProcessor
import logging
import app.utils as utils
import jsonpath_ng

logging.basicConfig(level=logging.DEBUG)
class TestProcessor(unittest.TestCase):

    def testCaptureJsonPath(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        pfile = PFile()
        pfile.response = Obj()
        pfile.response_text = '{"name":"John", "age":30, "car":null}';
        pfile.response_json = utils.str_to_json(pfile.response_text)
        pfile.response.headers = {
            'Date' : '20232323'
        }
        pfile.capture = {
            'test' : '@body jp $.name',
            'date' : '@headers Date'
        }
        processor = ResponseProcessor(pfile)
        processor.capture()

class Obj:
    pass