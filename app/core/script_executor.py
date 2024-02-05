from app.vars import vars
from app.args import args
import sys
import os
import logging as log

class ScriptExecutor:

    def execute(self, script, ctx):
        log.debug("executing script, \n%s", script)
        if isinstance(script, str):
            set = vars.set
            set_context =vars.set_context
            get = vars.get
            response = ctx.response
            file = ctx.file
            exec(script)

script_executor = ScriptExecutor()

class CtxFile:
    def __init__(self, parsed_data):
        for key in parsed_data:
            setattr(self, key, parsed_data[key])

class Ctx:
    def __init__(self, file, response=None):
        self.file = CtxFile(file)
        self.response = response