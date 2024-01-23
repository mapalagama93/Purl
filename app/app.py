from app import args

def main():
    # if -i flag enabled run initializer
    if args.is_init:
        from app.initializer import Initializer
        i = Initializer()
        i.init()
        exit()
    