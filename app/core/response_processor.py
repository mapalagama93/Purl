from app.vars import vars
import jsonpath_ng
import logging as log
import app.utils as utils

class ResponseProcessor:

    def __init__(self, file):
        self.file = file

    def capture(self):
        if self.file.capture == None:
            return
        
        for key, predicate in self.file.capture.items():
            if predicate.startswith('@body'):
                log.debug('capture body. predicate = %s', predicate)
                vars.set(key, self.__capture_body(predicate))
            if predicate.startswith('@headers'):
                log.debug('capture header. predicate = %s', predicate)
                vars.set(key, self.__capture_headers(predicate))
    
    def __capture_body(self, token):
        if self.file.response_json == None:
            return
        
        predicate = token.replace('@body ', '')
        if predicate.startswith('jsonpath'):
            log.debug('capture body with jsonpath. predicate = %s', predicate)
            return self.__get_from_jsonpath(self.file.response_json, predicate.replace('jsonpath ', ''))
        raise Exception('Invalid syntaxt for capture ' + token)
    
    def __get_from_jsonpath(self, json, path):
        log.debug('capture using jsonpath. jsonpath = %s', path)
        jp = jsonpath_ng.parse(path)
        match = jp.find(json)
        if len(match) > 0:
            log.debug('json path value found, path = %s, value = %s', path, match[0].value)
            return str(match[0].value)
        return ''

    def __capture_headers(self, token):
        if self.file.respon.headers == None:
            return
        predicate = token.replace('@headers ', '')
        return self.file.response.headers[predicate]