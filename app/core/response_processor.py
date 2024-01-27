from app.vars import vars
import jsonpath_ng
import logging as log
import app.utils as utils
from termcolor import cprint, colored

class ResponseProcessor:

    def __init__(self, file):
        self.file = file

    def capture(self):
        if self.file.capture == None:
            return
        print('')
        log.info('start capturing')
        for key, predicate in self.file.capture.items():
            val = self.__get_value(predicate)
            if val == None:
                print(colored('[Capture] value for ' + predicate + ' is empty', 'yellow'))
                continue
            print(colored('[Capture] ' + key + ' = ' + val, 'green'))
            vars.set(key, val)
    
    def asserts(self):
        if self.file.asserts == None:
            return None
        log.info('start assertions')
        self.all_asserts_status = True
        for key, token in self.file.asserts.items():
            log.info('asserting token = %s', token)
            ops = None
            expect = None
            actual = None
            if '|==|' in token:
                ops = '|==|'
            elif '|!=|' in token:
                ops = '|!=|'
            
            if ops == None:
                actual = self.__get_value(token)
                ops = '|!=|'
            else:
                t = token.split( ' ' + ops + ' ')[0]
                actual = self.__get_value(t)
                expect = token.split(' ' + ops + ' ')[1]
            result = False
            if ops == '|!=|':
                result = actual != expect
            elif ops == '|==|':
                result = actual == expect
                
            if result:
                print(colored('[Assert Success] ' + key + '' , 'green'))
            else:
                self.all_asserts_status = False
                print(colored('[Assert Failed] ' + key + ' | expected = ' + expect + ', actual value = ' + actual , 'red'))
        return self.all_asserts_status


    def __get_value(self, token):
        val = None
        if token.startswith('@body'):
            log.debug('getting  body value. predicate = %s', token)
            val = self.__capture_body(token)
        elif token.startswith('@headers'):
            log.debug('getting header value. predicate = %s', token)
            val = self.__capture_headers(token)
        elif token.startswith('@status') :
            val = str(self.file.response_status)
        elif token.startswith('@duration') :
            val = self.file.response_time
        return val

    def __capture_body(self, token):
        predicate = token.replace('@body ', '')
        if predicate.startswith('jsonpath') and self.file.response_json != None:
            log.debug('capture body with jsonpath. predicate = %s', predicate)
            return self.__get_from_jsonpath(self.file.response_json, predicate.replace('jsonpath ', ''))
        return None
    
    def __get_from_jsonpath(self, json, path):
        log.debug('capture using jsonpath. jsonpath = %s', path)
        try:
            jp = jsonpath_ng.parse(path)
        except:
            raise Exception('Unable to parse jsonpath "' + path + '" , check for syntax errors' )
        match = jp.find(json)
        if len(match) > 0:
            log.debug('json path value found, path = %s, value = %s', path, match[0].value)
            return str(match[0].value)
        return None

    def __capture_headers(self, token):
        if self.file.response.headers == None:
            return None
        predicate = token.replace('@headers ', '')
        return self.file.response.headers[predicate] if predicate in self.file.response.headers else None