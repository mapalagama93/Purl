from app.vars import vars
import sys
import os
import logging as log

class ScriptExecutor:

    def execute(self, script):
        log.debug("executing script, \n%s", script)
        if isinstance(script, str):
            exec(script)

script_executor = ScriptExecutor()