from app.args import args

def main():
    # if -i flag enabled run initializer
    args.parse()
    if args.is_init:
        from app.initializer import Initializer
        i = Initializer()
        i.init()
        exit()
    
    from app.core.processor import processor
    processor.process(args.files)
    