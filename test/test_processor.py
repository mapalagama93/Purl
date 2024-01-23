from app.vars import vars 
import unittest
import os
from app.args import args
from app.core.processor import processor
import logging
from pprint import pprint

class TestProcessor(unittest.TestCase):

    def testAllSections(self):
        logging.basicConfig(level=logging.DEBUG)
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor.process(['api_get_with_prescript.purl'])