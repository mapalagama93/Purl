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
        log.info('reading file = %s', self.pfile.file_path)
        with open(self.pfile.file_path, 'r') as content:
            self.pfile.file_content = content.read()
        return self.pfile
    
    def __parse_file_content(self):
        log.debug('replacing file content variables')
        content = self.pfile.file_content
        vals = vars.get_all()
        for v in vals:
            content =  content.replace('${' + v + '}', str(vals[v].data))
        # catch missing parametrs
        regex = r"\${(\w+)}"
        matches = re.finditer(regex,  content, re.MULTILINE)
        errors = []
        for m in matches:
            errors.append("${"+m.group(1)+"}")
        if len(errors) > 0:
            raise Exception('Unknown values for variables ' + utils.obj_to_json_string(errors))
        return content

    def parse_file(self):
        data = utils.str_to_yaml(self.__parse_file_content())
        self.pfile.url = data['Endpoint'] if 'Endpoint' in data else None
        self.pfile.method = data['Method'] if 'Method' in data else None
        self.pfile.basic_auth = data['BasicAuth'] if 'BasicAuth' in data else None
        self.pfile.headers = data['Headers'] if 'Headers' in data else None
        self.pfile.path_params = data['PathParams'] if 'PathParams' in data else None
        self.pfile.query_params = data['QueryParams'] if 'QueryParams' in data else None
        self.pfile.json_body = utils.str_to_json(data['JsonBody']) if 'JsonBody' in data else None
        self.pfile.form_params = data['FormParams'] if 'FormParams' in data else None
        self.pfile.multipart_data = data['MultipartData'] if 'MultipartData' in data else None
        self.pfile.capture = data['Capture'] if 'Capture' in data else None
        self.pfile.options = data['Options'] if 'Options' in data else None
        self.pfile.asserts = data['Asserts'] if 'Asserts' in data else None
        self.pfile.text_body =  data['TextBody'] if 'TextBody' in data else None
        self.pfile.pre_script =  data['PreScript'] if 'PreScript' in data else None
        self.pfile.post_script =  data['PostScript'] if 'PostScript' in data else None
        return self.pfile