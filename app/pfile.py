
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