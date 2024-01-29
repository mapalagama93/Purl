from app.vars import vars
from app.args import args
import sys
import os
import logging as log

class ScriptExecutor:

    def execute(self, script):
        log.debug("executing script, \n%s", script)
        if isinstance(script, str):
            set = vars.set
            get = vars.get
            exec(script)

script_executor = ScriptExecutor()