from app.vars import vars 
import unittest
import os
from app.args import args
from app.core.processor import processor
import logging
# logging.basicConfig(level=logging.DEBUG)
class TestProcessor(unittest.TestCase):

    def testGetPreScript(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor.process(['api_get_with_prescript.purl'])

    def testFormParams(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor.process(['api_post_form_params.purl'])

    def testQueryParams(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor.process(['api_post_query_params.purl'])

    def testPathParams(self):
        args.root = os.path.abspath(os.getcwd() + '/test/resources')
        args.env = []
        vars.init()
        processor.process(['api_post_path_params.purl'])