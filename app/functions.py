import string
import random
import base64
from datetime import datetime
import hashlib
import uuid as uid

STD_DATE = '%Y-%m-%d'
STD_TIME = '%H:%M:%S'

def rand_num(length=5, points=0):
    num = ''.join(random.choices(string.digits, k=length))
    if(points > 0):
        num += '.' + ''.join(random.choices(string.digits, k=points))
    return num

def rand_str(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    return base64.b64decode(text.encode()).decode()

def time(data=datetime.now(), format='%Y-%m-%dT%H:%M:%S'):
    return data.strftime(format)

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def uuid():
    return str(uid.uuid4())

