from app.args import args
from app.core.file_processor import FileProcessor
from app.core.curl_generator import CurlGenerator
from app.core.request_processor import RequestProcessor
from app.core.response_processor import ResponseProcessor
from app.core.script_executor import script_executor
import logging as log
from termcolor import cprint

class Processor:

    def process(self, files):
        if len(files) == 0:
            cprint('No filew provided. eg: purl -f request.purl', 'black', 'on_yellow', attrs=['bold'])

        for file in files:
            cprint('\n Running ' + file + '', 'white', 'on_blue', attrs=['bold'])
            log.info('processing file, file = %s', __file__)
            file_processor = FileProcessor(file)
            try:
                pfile = file_processor.parse_pre_script()
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
            else:
                request_processor = RequestProcessor(pfile)
                try:
                    request_processor.process()
                except Exception as e:
                    cprint(' UNEXPECTED EXCEPTION ', 'white', 'on_red', attrs=['bold'])
                    cprint(str(e), 'light_yellow')
                    exit()
            
            response_processor = ResponseProcessor(pfile)
            response_processor.capture()
            
processor = Processor()