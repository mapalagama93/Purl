from app.args import args
from app.vars import vars

class PFile:
    
    file_path = None
    file_content = None
    parsed_data = None

    # request vars
    method = None
    url = None
    status = 200
    basic_auth = None
    path_params = {}
    query_params = {}
    headers = {}
    json_body = None
    text_body = None 
    form_params = None
    multipart_data = None
    capture = None
    options = {}
    asserts = {}
    pre_script = None 
    post_script = None

    # response vars
    response = None
    response_json = None
    response_text = None 
    response_status = None
    response_time = None

    __all_options = None

    def get_full_url(self):
        url = self.url
        if self.path_params:
            for x in self.path_params:
                url = url.replace(':' + x, str(self.path_params[x]))
        return url

    def get_full_headers(self):
        if 'setContentType' in self.options and self.options['setContentType']:
            return self.headers
        
        if self.get_content_type() == None:
            return self.headers

        for k, v in self.headers.items():
            if k.lower() == 'content-type':
                return self.headers

        return {**self.headers, **{'Content-Type' : self.get_content_type()}}

    def get_content_type(self):
        if self.json_body:
            return 'application/json'
        elif self.form_params:
            return 'application/x-www-form-urlencoded'
        elif self.multipart_data:
            return 'multipart/form-data'
        elif self.text_body:
            return 'text/plain'
        return None
    
    def get_option(self, key, defaultValue = None):
        if self.__all_options == None:
            ops = {}
            vs = vars.get_all()
            for v in vs:
                if v.startswith('purl_ops_'):
                    ops[v.replace('purl_ops_', '').lower()] = str(vs[v].data)
            
            for k,v in self.options.items():
                ops[k.lower()] = str(v)

            for i in args.options:
                if '=' not in i:
                    raise Exception('Invalid option and value ' + i)
                s = i.split('=')
                ops[s[0].lower()] = str(s[1])
            self.__all_options = ops

        return self.__all_options[key.lower()] if key.lower() in self.__all_options else defaultValue

    def get_timeout(self):
        try:
            return float(self.get_option('timeout', 60))
        except:
            raise('Invalid timeout value')
    def is_option_set_to(self, option, value):
        return self.get_option(option, None) == value
    
    def get_verify_ssl(self):
        return self.get_option('insecure', 'false').lower() != 'true'