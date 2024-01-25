from app.vars import vars 
import unittest
import os
from app.args import args
from app.core.file_processor import FileProcessor
import logging
from pprint import pprint

class TestFileProcessor(unittest.TestCase):

    def testParse1(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor = FileProcessor('test_basic.purl')
        pfile = processor.pfile
        self.assertIsNotNone(pfile.file_content)

    
    def testNoMethod(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor = FileProcessor('test_no_method.purl')
        self.assertRaises(Exception, processor.parse_file)

    def testNoUrl(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor = FileProcessor('test_no_url.purl')
        self.assertRaises(Exception, processor.parse_file)

    def testCaptureBetween(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor = FileProcessor('test_capture_between.purl')
        pfile = processor.parse_file()
        self.assertIsNotNone(pfile.headers)
        

    def testCaptureEnd(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor = FileProcessor('test_capture_end.purl')
        pfile = processor.parse_file()
        self.assertIsNotNone(pfile.headers)


    def testAllSectionsVar(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        vars.set('scema', 'https')
        vars.set('p1', '1')
        vars.set('p2', '1')
        processor = FileProcessor('test_all_sections.purl')
        pfile = processor.parse_file()
        print(pfile.file_content)