from app.args import args
from app.pfile import PFile
import app.utils as utils
import re
import logging as log
from app.vars import vars

class FileProcessor:


    def __init__(self, file):
        self.file = file
        self.read_file()

    def read_file(self):
        self.pfile = PFile()
        self.pfile.file_path = utils.get_abs_file_path(self.file)
        log.debug('reading file = %s', self.pfile.file_path)
        with open(self.pfile.file_path, 'r') as content:
            self.pfile.file_content = content.read()
        return self.pfile
    
    def __parse_file_content(self):
        log.debug('replacing file content variables')
        content = self.pfile.file_content
        vals = vars.get_all()
        for v in vals:
            content =  content.replace('${' + v + '}', str(vals[v].data))
        return content

    def parse_file(self):
        data = utils.str_to_yaml(self.__parse_file_content())
        self.pfile.url = data['Endpoint'] if 'Endpoint' in data else None
        self.pfile.method = data['Method'] if 'Method' in data else None
        self.pfile.status = data['Status'] if 'Status' in data else "200"
        self.pfile.basic_auth = data['BasicAuth'] if 'BasicAuth' in data else None
        self.pfile.headers = data['Headers'] if 'Headers' in data else {}
        self.pfile.path_params = data['PathParams'] if 'PathParams' in data else {}
        self.pfile.query_params = data['QueryParams'] if 'QueryParams' in data else {}
        self.pfile.json_body = utils.str_to_json(data['JsonBody']) if 'JsonBody' in data else None
        self.pfile.form_params = data['FormParams'] if 'FormParams' in data else None
        self.pfile.multipart_data = data['MultipartData'] if 'MultipartData' in data else None
        self.pfile.capture = data['Captures'] if 'Captures' in data else {}
        self.pfile.options = data['Options'] if 'Options' in data else {}
        self.pfile.asserts = data['Asserts'] if 'Asserts' in data else {}
        self.pfile.text_body =  data['TextBody'] if 'TextBody' in data else None
        self.pfile.pre_script =  data['PreScript'] if 'PreScript' in data else None
        self.pfile.post_script =  data['PostScript'] if 'PostScript' in data else None
        return self.pfile