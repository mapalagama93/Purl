from app.args import args
from app.core.file_processor import file_processor
from app.core.script_executor import script_executor
import logging as log

class Processor:
    
    def process(self, files):

        for file in files:
            try:
                log.info('processing file, file = %s', __file__)
                pfile = file_processor.get_pfile(file)
                file_processor.parse_pre_script(pfile)
            except Exception as ex:
                log.error('error while parsing file = %s, message = %s', file, ex)
                continue
            
            if pfile.pre_script:
                log.info('executing prescript, file = %s', file)
                script_executor.execute(pfile.pre_script)

            pfile = file_processor.parse_pfile(pfile)
            
processor = Processor()