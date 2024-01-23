from app.vars import vars 
import unittest
import os
from app.args import args
from app.core.file_processor import file_processor
import logging
from pprint import pprint

class TestFileProcessor(unittest.TestCase):

    def testParse1(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        pfile = file_processor.get_pfile('test_basic.purl')
    
    def testNoMethod(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        self.assertRaises(Exception, file_processor.get_pfile, 'test_no_method.purl')

    def testNoUrl(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        self.assertRaises(Exception, file_processor.get_pfile, 'test_no_url.purl')

    def testCaptureBetween(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        pfile = file_processor.get_pfile('test_capture_between.purl')
        self.assertIsNotNone(pfile.headers)

    def testCaptureEnd(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        pfile = file_processor.get_pfile('test_capture_end.purl')
        self.assertIsNotNone(pfile.headers)

    def testAllSections(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        pfile = file_processor.get_pfile('test_all_sections.purl')