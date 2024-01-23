from app.vars import vars 
import unittest
import os
from types import SimpleNamespace

class TestVars(unittest.TestCase):

    def test_init_no_files(self):
        args = SimpleNamespace()
        args.root = os.getcwd()
        args.env = []
        vars.init(args)
        self.assertEqual(vars.get('no_key', 'sample value'), 'sample value')
    
    def test_init_no_env(self):
        args = SimpleNamespace()
        args.root = os.getcwd() + '/test/resources'
        args.env = []
        vars.init(args)
        self.assertEqual(vars.get('value1', 'sample value'), 'from config value1')
        self.assertEqual(vars.get('value2', 'sample value'), 'from store value2')

    def test_init_env(self):
        args = SimpleNamespace()
        args.root = os.getcwd() + '/test/resources'
        args.env = ['dev']
        vars.init(args)
        self.assertEqual(vars.get('value1', 'sample value'), 'from env value1')
    
    def test_init_set_store(self):
        args = SimpleNamespace()
        args.root = os.getcwd() + '/test/resources'
        args.env = ['dev']
        vars.init(args)
        self.assertEqual(vars.get('value1', 'sample value'), 'from env value1')
        vars.set('value3', 'new value')
        self.assertEqual(vars.get('value3', 'sample value'), 'new value')

    def test_init_set_context(self):
        args = SimpleNamespace()
        args.root = os.getcwd() + '/test/resources'
        args.env = ['dev']
        vars.init(args)
        vars.set_context('value4', 'context value')
        self.assertEqual(vars.get('value4', 'sample value'), 'context value')