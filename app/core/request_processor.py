from requests import request
import app.utils as utils
import logging as log
from termcolor import cprint, colored

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
        log.info('sending http requests to url = %s', url)
        self.__log_request()
        self.response = request(method, url, data=data, json=json, params=query_params, headers=headers)
        self.file.response = self.response
        log.info('response received. status = %s', self.response.status_code)

    def __get_url(self):
        url = self.file.url
        if self.file.path_params:
            for x in self.file.path_params:
                url = url.replace(':' + x, str(self.file.path_params[x]))
        log.info('prepare url, url = %s', url)
        return url
    def __get_query_params(self):
        if self.file.query_params:
            log.info('prepare query params')
            return self.file.query_params
        
    def __get_headers(self):
        if self.file.headers:
            log.info('prepare headers')
            return self.file.headers
        return {}

    def __get_json(self):
        if self.file.json_body:
            log.info('prepare json body')
            return utils.obj_to_json_string(self.file.json_body)
        return None

    def __get_data(self):
        if self.file.text_body:
            log.info('prepare plain text body')
            return self.file.text_body
        if self.file.form_params:
            log.info('prepare form params')
            return self.file.form_params

    def __log_request(self):
        cprint(' REQUEST ', 'black', 'on_blue')
        print(colored(self.file.method, 'blue', attrs=['bold']), colored(self.__get_url(), attrs=['bold']))
        print(colored('Request Headers ', 'magenta', attrs=['bold']))
        for k, v in self.__get_headers().items():
            print(colored(k, attrs=['bold']), ':', colored(v))
        # print(colored('Request Body ', 'magenta', attrs=['bold']), 
        #       colored('[JSON]' if self.__is_json_request() and self.__data() != None else '', 'light_grey', attrs=['bold']), '\n', 
        #       data, sep="")
        print('\n')
    
    def __log_response(self):
        cprint(' RESPONSE ', 'black', 'on_green')
        print(colored('Status', 'magenta', attrs=['bold']), self.response['status'])
        print(colored('Response Body ', 'magenta', attrs=['bold']), '\n', 
              json.dumps(self.response['data'], indent=2) if self.__is_json_response() and self.response['json'] else self.response['data'], sep="")
        print(colored('Response Headers ', 'magenta', attrs=['bold']), '\n' , json.dumps(self.response['headers'], indent=2))