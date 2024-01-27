from app.args import args
from app.core.file_processor import FileProcessor
from app.core.curl_generator import CurlGenerator
from app.core.request_processor import RequestProcessor
from app.core.response_processor import ResponseProcessor
from app.core.script_executor import script_executor
import logging as log
from termcolor import cprint, colored

class Processor:

    def process(self, files):
        if len(files) == 0:
            cprint('No filew provided. eg: purl -f request.purl', 'black', 'on_yellow', attrs=['bold'])

        for file in files:
            print(colored('  ', 'white', 'on_blue', attrs=["bold"]) + 
                  colored(' REQUEST ', 'blue', 'on_white', attrs=['bold']) + 
                  colored(' ' + file + ' ', 'white', 'on_dark_grey', attrs=['bold']))
            log.info('processing file, file = %s', __file__)
            file_processor = FileProcessor(file)
            try:
                pfile = file_processor.parse_file()
            except Exception as ex:
                log.error('error while parsing file = %s, message = %s', file, ex)
                continue
            if pfile.pre_script:
                log.info('executing prescript, file = %s', file)
                script_executor.execute(pfile.pre_script)

            pfile = file_processor.parse_file()

            if args.is_curl:
               curl_generator = CurlGenerator(pfile)
               curl_generator.generate_curl()
               exit()
           
            try:
                request_processor = RequestProcessor(pfile)
                request_processor.process()
                response_processor = ResponseProcessor(pfile)
                response_processor.asserts()
                if response_processor.all_asserts_status:
                    response_processor.capture()
            except Exception as e:
                cprint(' UNEXPECTED EXCEPTION ', 'white', 'on_red', attrs=['bold'])
                cprint(str(e), 'light_yellow')
                if args.is_debug:
                    raise e
                exit()
            
processor = Processor()