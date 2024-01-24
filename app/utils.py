from app.args import args
import os
import json
import yaml

def get_abs_file_path(path):
    return os.path.abspath(args.root + '/' + path);

def is_file_exists(path):
    return os.path.exists(get_abs_file_path(path));

def str_to_json(text):
    return json.loads(text)

def obj_to_json_string(obj, pretty=False):
    if pretty:
        return json.dumps(obj, indent=2)
    return json.dumps(obj)

def str_to_yaml(text):
    return yaml.safe_load(text)

def status_description(status):
    data = {"100":"Continue","101":"Switching Protocols","102":"Processing","200":"OK","201":"Created","202":"Accepted","203":"Non-Authoritative Information","204":"No Content","205":"Reset Content","206":"Partial Content","207":"Multi-Status","226":"IM Used","300":"Multiple Choices","301":"Moved Permanently","302":"Found","303":"See Other","304":"Not Modified","305":"Use Proxy","307":"Temporary Redirect","308":"Permanent Redirect","400":"Bad Request","401":"Unauthorized","402":"Payment Required","403":"Forbidden","404":"Not Found","405":"Method Not Allowed","406":"Not Acceptable","407":"Proxy Authentication Required","408":"Request Timeout","409":"Conflict","410":"Gone","411":"Length Required","412":"Precondition Failed","413":"Payload Too Large","414":"URI Too Long","415":"Unsupported Media Type","416":"Range Not Satisfiable","417":"Expectation Failed","418":"I'm a teapot","422":"Unprocessable Entity","423":"Locked","424":"Failed Dependency","426":"Upgrade Required","428":"Precondition Required","429":"Too Many Requests","431":"Request Header Fields Too Large","451":"Unavailable For Legal Reasons","500":"Internal Server Error","501":"Not Implemented","502":"Bad Gateway","503":"Service Unavailable","504":"Gateway Time-out","505":"HTTP Version Not Supported","506":"Variant Also Negotiates","507":"Insufficient Storage","511":"Network Authentication Required","1xx":"**Informational**","2xx":"**Successful**","3xx":"**Redirection**","4xx":"**Client Error**","5xx":"**Server Error**","7xx":"**Developer Error**"}
    return data[status]