
class PFile:
    
    file_path = None
    file_content = None;

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

    def get_full_url(self):
        url = self.url
        if self.path_params:
            for x in self.path_params:
                url = url.replace(':' + x, str(self.path_params[x]))
        return url

    def get_full_headers(self):
        if 'set_default_content_type' in self.options and self.options['set_default_content_Type']:
            return self.headers
        
        for k, v in self.headers.items():
            if k.lower() == 'content-type':
                return self.headers
        return {**self.headers, **{'content-type' : self.get_content_type()}}

    def get_content_type(self):
        if self.json_body:
            return 'application/json'
        elif self.form_params:
            return 'application/x-www-form-urlencoded'
        elif self.multipart_data:
            return 'tform-data/multipart'
        return 'text/plain'
        