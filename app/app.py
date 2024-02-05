from app.args import args
from app.vars import vars
import logging
import warnings

def main():
    warnings.filterwarnings("ignore")
    args.parse()
    if args.is_debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.is_init:
        from app.initializer import Initializer
        i = Initializer()
        i.init()
        exit(0)
    
    from app.core.processor import processor
    vars.init()
    processor.process_files(args.files)
    