from requests import request
import app.utils as utils
import logging as log
from termcolor import colored
from requests_toolbelt import MultipartEncoder

class RequestProcessor:

    def __init__(self, pfile):
        self.file = pfile

    def process(self):
        method = self.file.method
        url = self.file.get_full_url()
        headers = self.__get_headers()
        data = self.__get_json() if self.__get_json() else self.__get_data()
        query_params = self.__get_query_params()
        log.debug('sending http requests to url = %s', url)
        self.__log_request()
        self.response = request(method, 
                                url, 
                                data=data, 
                                params=query_params, 
                                headers=headers, 
                                verify=self.file.get_verify_ssl(),
                                timeout=self.file.get_timeout()
                                )
        self.file.response = self.response
        self.__set_response()
        self.__log_response()
        log.debug('response received. status = %s', self.response.status_code)


    
    def __set_response(self):
        try:
            self.file.response_json = self.response.json()
            self.file.response_text = self.response.text
        except:
            self.file.response_json = None
            self.file.response_text = self.response.text
        self.file.response_status = self.response.status_code
        self.file.response_time = str(self.response.elapsed.microseconds / 1000)

    def __get_query_params(self):
        if self.file.query_params:
            log.debug('prepare query params')
            return self.file.query_params
        return None
        
    def __get_headers(self):
        return self.file.get_full_headers()

    def __get_json(self):
        if self.file.json_body:
            log.debug('prepare json body')
            return utils.obj_to_json_string(self.file.json_body)
        return None

    def __get_data(self):
        if self.file.text_body:
            log.debug('prepare plain text body')
            return self.file.text_body
        if self.file.form_params:
            log.debug('prepare form params')
            return self.file.form_params
        if self.file.multipart_data:
            log.debug('prepare multipart data')
            return self.__get_multipart_data()
    
    def __get_multipart_data(self):
        if self.file.multipart_data == None:
            return {}
        fields = {}
        for k, v in self.file.multipart_data.items():
            if not v.startswith('@file://'):
                fields[k] =  v
                continue
            
            s = v.split(' | ')
            if len(s) != 3:
                raise Exception('Invalid multipart file syntaxt ' + v)
            file = s[0].replace('@file://', '')
            name = s[1]
            type = s[2]
            fields[k] = (name, open(file, 'rb'), type)
        print(fields)
        return MultipartEncoder(fields=fields)

    def __log_request(self):
        print('')
        print(colored(' ' + self.file.method + ' ', 'white', 'on_magenta', attrs=['bold']), 
              colored(self.file.get_full_url(), attrs=['bold']))
        print('')
        # print headers
        print(colored('Request Headers ', 'magenta', attrs=['bold']))
        headers = self.__get_headers()
        if len(headers) == 0:
            print(colored('None', attrs=['bold']))
        for k, v in headers.items():
            print(colored(k, attrs=['bold']), ':', colored(v))
        print('')
        # print body
        type = ''
        data = 'None'
        if self.file.json_body:
            type = '[JSON]'
            data = utils.obj_to_json_string(self.file.json_body, pretty=True)
        elif self.file.form_params:
            type = '[FORM]'
            data = ''
            for k, v in self.file.form_params.items():
                data += colored(k, attrs=['bold'])
                data += ' : '
                data += colored(v)
                data += '\n'
            data = data[:-1]

        elif self.file.text_body:
            type = '[TEXT]'
            data = self.file.text_body
        elif self.file.multipart_data:
            type = '[MULTIPART]'
            data = ''
            for k, v in self.file.multipart_data.items():
                data += colored(k, attrs=['bold'])
                data += ' : '
                data += colored(v)
                data += '\n'
            data = data[:-1]
        
        print(colored('Request Body ' + type, 'magenta', attrs=['bold']))
        print(colored(data))
        print('')
    
    def __log_response(self):
        print(  colored('  ', 'white', 'on_green', attrs=["bold"]) +
                colored(' RESPONSE ', 'green', 'on_white', attrs=["bold"]) + 
                colored(' ' + str(self.response.status_code) + ' ' + 
                        utils.status_description(str(self.response.status_code)) + 
                        ' [' + '' + str(self.file.response_time) + ' ms' + '] ', 'white', 'on_dark_grey', attrs=['bold']))
        print('')
        # print response body
        body = self.file.response_text
        if self.file.response_json:
            body = utils.obj_to_json_string(self.response.json(), pretty=True)
            
        print(colored('Response Body ', 'magenta', attrs=['bold']))
        print(colored(body, 'light_grey'))
        print('')
        # print response header
        print(colored('Response Headers ', 'magenta', attrs=['bold']))
        headers = self.response.headers
        if len(headers) == 0:
            print(colored('None', attrs=['bold']))
        skipped_header_count = 0
        for k, v in headers.items():
            if k.lower() in utils.get_std_response_headers() and not self.file.is_option_set_to('showAllHeaders', 'true'):
                skipped_header_count += 1
                continue
            print(colored(k, attrs=['bold']), ':', colored(v))
        if skipped_header_count > 0:
            print('')
            print(colored('[' + str(skipped_header_count) + ' Hidden headers]', 'light_grey'))

        print('')