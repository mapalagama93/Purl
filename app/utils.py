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

def str_to_yaml(text):
    return yaml.safe_load(text)