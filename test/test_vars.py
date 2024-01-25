from app.vars import vars 
import unittest
import os
from types import SimpleNamespace
from app.args import args

class TestVars(unittest.TestCase):

    def test_init_no_files(self):
        args.root = os.getcwd()
        args.env = []
        vars.init()
        self.assertEqual(vars.get('no_key', 'sample value'), 'sample value')
    
    def test_init_no_env(self):
        args.root = os.getcwd() + '/test/resources'
        args.env = []
        vars.init()
        self.assertEqual(vars.get('value1', 'sample value'), 'from config value1')
        self.assertEqual(vars.get('value2', 'sample value'), 'from store value2')

    def test_init_env(self):
        args.root = os.getcwd() + '/test/resources'
        args.env = ['dev']
        vars.init()
        self.assertEqual(vars.get('value1', 'sample value'), 'from env value1')
    
    def test_init_set_store(self):
        args.root = os.getcwd() + '/test/resources'
        args.env = ['dev']
        vars.init()
        self.assertEqual(vars.get('value1', 'sample value'), 'from env value1')
        vars.set('value3', 'new value')
        self.assertEqual(vars.get('value3', 'sample value'), 'new value')

    def test_init_set_context(self):
        args.root = os.getcwd() + '/test/resources'
        args.env = ['dev']
        vars.init()
        vars.set_context('value4', 'context value')
        self.assertEqual(vars.get('value4', 'sample value'), 'context value')

    
    def test_init_set_context_asd(self):
        import yaml
        import json
        r = open('test/resources/api_get_json_capture.yaml', 'r').read()
        y = yaml.safe_load(r)
        print(json.dumps(json.loads(y['JsonBody']), indent=2))
