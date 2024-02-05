import app.utils as utils
from urllib.parse import urlencode
from termcolor import cprint, colored
import logging as log
class CurlGenerator:

    def __init__(self, file):
        self.file = file

    def generate_curl(self):
        print('')
        cmd = 'curl -X '
        cmd += self.file.method + ' ' + self.__get_url() + ' \\\n'
        cmd += self.__get_headers()
        cmd += self.__get_body()
        cmd += ''
        last2Char = cmd[-2:]
        if last2Char == '\\\n':
            cmd = cmd[:-2]
        cprint(cmd)
    
    def __get_url(self):
        if self.file.query_params:
            return self.file.get_full_url() + '?' + urlencode(self.file.query_params)
        return self.file.get_full_url()

    def __get_headers(self):
        header = '';
        for k, v in self.file.get_full_headers().items():
            header += "-H '" + k + ": " + v + "' \\\n"
        return header

    def __get_body(self):
        if self.file.json_body != None:
            log.debug('adding json body to curl')
            return "-d '"+utils.obj_to_json_string(self.file.json_body, pretty=True)+"' "
        elif self.file.form_params:
            log.debug('adding form params to curl')
            return "-d '" + urlencode(self.file.form_params) + "' "
        elif self.file.text_body:
            log.debug('adding text body to curl')
            return "-d '" + self.file.text_body + "' "
        if self.file.method != 'GET':
            log.debug('request object is empty. adding empty -d to curl')
            return "-d ''"
        log.debug('no body added to the request')
        return ''