from requests import request
import app.utils as utils
import logging as log

class RequestProcessor:

    def __init__(self, pfile):
        self.file = pfile

    def process(self):
        method = self.file.method
        url = self.__get_url()
        headers = self.__get_headers()
        json = self.__get_json()
        data = self.__get_data()
        query_params = self.__get_query_params()
        request(method, url, data=data, json=json, params=query_params, headers=headers)

    def __get_url(self):
        url = self.file.url
        if self.file.path_param:
            for x in self.file.path_param:
                url = url.replace(':' + x, str(self.file.path_param[x]))
        log.info('prepare url, url = %s', url)
        return url

    def __get_headers(self):
        if self.file.headers:
            return self.file.headers
        return {}

    def __get_json(self):
        if self.file.jsonBoby:
            log.info('prepare json body')
            return utils.obj_to_json_string(self.file.jsonBoby)
        return None

    def __get_data(self):
        if self.file.TextBody:
            log.info('prepare plain text body')
            return self.file.TextBody
        if self.file.formParams:
            log.info('prepare form params')
            return self.file.formParams
        

request_processor = RequestProcessor()