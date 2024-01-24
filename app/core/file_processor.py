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
        log.info('reading file %s', self.pfile.file_path)
        self.pfile.file_content = open(self.pfile.file_path, 'r').read()
        return self.pfile
    
    def parse_pre_script(self):
        self.pfile.pre_script = self.get_content_for(self.pfile.file_content, "PreScript")
        return self.pfile
    
    def __parse_file_content(self):
        vals = vars.get_all()
        for v in vals:
            self.pfile.file_content =  self.pfile.file_content.replace('{{' + v + '}}', str(vals[v]))
        # catch missing parametrs
        regex = r"{{(\w+)}}"
        matches = re.finditer(regex,  self.pfile.file_content, re.MULTILINE)
        errors = []
        for m in matches:
            errors.append("{{"+m.group(1)+"}}")
        if len(errors) > 0:
            raise Exception('Unknown values for variables ' + utils.obj_to_json_string(errors))

    def parse_file(self):
        self.__parse_file_content()
        print(self.pfile.file_content)
        self.__set_method_url()
        basic_auth = self.get_content_for("BasicAuth")
        if basic_auth:
            self.pfile.basic_auth = utils.str_to_yaml(basic_auth)

        headers = self.get_content_for("Headers")
        if headers:
            self.pfile.headers = utils.str_to_yaml(headers)

        query_params = self.get_content_for("QueryParams")
        if query_params:
            self.pfile.query_params = utils.str_to_yaml(query_params)

        json_body = self.get_content_for("JsonBody")
        if json_body != None:
            self.pfile.json_body = utils.str_to_json(json_body)

        form_params = self.get_content_for("FormParams")
        if form_params:
            self.pfile.form_params = utils.str_to_yaml(form_params)
     
        multipart_data = self.get_content_for("MultipartData")
        if multipart_data:
            self.pfile.multipart_data = utils.str_to_yaml(multipart_data)

        capture = self.get_content_for("Capture")
        if capture:
            self.pfile.capture = utils.str_to_yaml(capture)

        options = self.get_content_for("Options")
        if options:
            self.pfile.options = utils.str_to_yaml(options)

        asserts = self.get_content_for("Asserts")
        if asserts:
            self.pfile.asserts = utils.str_to_yaml(asserts)
            

        self.pfile.text_body = self.get_content_for("TextBody")
        self.pfile.pre_script = self.get_content_for("PreScript")
        self.pfile.post_script = self.get_content_for("PostScript")
        return self.pfile
    
    def __set_method_url(self):
        try:
            regex = r"((GET|POST|PATCH|DELETE|PUT))\s+((htt|{{).*)\s+"
            matches = re.search(regex, self.pfile.file_content, re.MULTILINE)
            self.pfile.url = matches.group(3)
            self.pfile.method = matches.group(2)
            if(self.pfile.url == None or self.pfile.method == None):
                raise Exception()
            log.debug('captured url %s', self.pfile.url)
            log.debug('captured method %s', self.pfile.method)
        except Exception as error:
            raise Exception('Cannot find method and url')


    def get_content_for(self, tag, defaultValue=None):
        text = self.pfile.file_content
        regex = r"\[" + tag +"\]\s((.|\n|\r\n)*?)\["
        matches = re.search(regex, text, re.MULTILINE)
        if matches:
            content = matches.group(1)
            log.debug('tag content found in between for  \n[%s]\n%s\n', tag, content)
            return content
        
        regex = r"\["+tag+"\]\s((.|\n|\r\n)*)"
        matches = re.search(regex, text, re.MULTILINE)
        if matches:
            content = matches.group(1)
            log.debug('tag content found end for \n[%s]\n%s\n', tag, content)
            return content
        return defaultValue