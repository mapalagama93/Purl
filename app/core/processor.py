from app.args import args
from app.core.file_processor import FileProcessor
from app.core.request_processor import RequestProcessor
from app.core.script_executor import script_executor
import logging as log

class Processor:
    
    def process(self, files):

        for file in files:
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
            request_processor = RequestProcessor(pfile)
            request_processor.process()
            
processor = Processor()