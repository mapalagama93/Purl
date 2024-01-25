from app.args import args
from app.vars import vars
import logging

def main():
    # if -i flag enabled run initializer
    args.parse()

    if args.is_debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.is_init:
        from app.initializer import Initializer
        i = Initializer()
        i.init()
        exit()
    
    from app.core.processor import processor
    vars.init()
    processor.process(args.files)
    