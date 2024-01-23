from app.args import args
from app.pfile import PFile
import app.utils as utils
import re
import logging as log

class FileProcessor:

    def get_pfile(self, file):
        pfile = PFile()
        pfile.filePath = utils.get_abs_file_path(file)
        pfile.fileContent = self.read_file(pfile.filePath)
        self.parse_pfile(pfile)
        return pfile
    
    def parse_pfile(self, pfile):
        self.__set_method_url(pfile)

        basicAuth = self.get_content_for(pfile.fileContent, "BasicAuth")
        if basicAuth:
            pfile.basicAuth = utils.str_to_yaml(basicAuth)

        headers = self.get_content_for(pfile.fileContent, "Headers")
        if headers:
            pfile.headers = utils.str_to_yaml(headers)

        queryStringParams = self.get_content_for(pfile.fileContent, "QueryStringParams")
        if queryStringParams:
            pfile.queryStringParams = utils.str_to_yaml(queryStringParams)

        jsonBody = self.get_content_for(pfile.fileContent, "JsonBody")
        if jsonBody != None:
            pfile.jsonBody = utils.str_to_json(jsonBody)

        formParams = self.get_content_for(pfile.fileContent, "FormParams")
        if formParams:
            pfile.formParams = utils.str_to_yaml(formParams)
     
        multipartFormData = self.get_content_for(pfile.fileContent, "MultipartFormData")
        if multipartFormData:
            pfile.multipartFormData = utils.str_to_yaml(multipartFormData)

        capture = self.get_content_for(pfile.fileContent, "Capture")
        if capture:
            pfile.capture = utils.str_to_yaml(capture)

        options = self.get_content_for(pfile.fileContent, "Options")
        if options:
            pfile.options = utils.str_to_yaml(options)

        asserts = self.get_content_for(pfile.fileContent, "Asserts")
        if asserts:
            pfile.asserts = utils.str_to_yaml(asserts)
            

        pfile.xmlBody = self.get_content_for(pfile.fileContent, "XmlBody")
        pfile.plainTextBody = self.get_content_for(pfile.fileContent, "PlainTextBody")
        pfile.preScript = self.get_content_for(pfile.fileContent, "PreScript")
        pfile.postScript = self.get_content_for(pfile.fileContent, "PostScript")
    
    def __set_method_url(self, pfile):
        try:
            regex = r"((GET|POST|PATCH|DELETE|PUT))\s+((htt|{{).*)\s+"
            matches = re.search(regex, pfile.fileContent, re.MULTILINE)
            pfile.url = matches.group(3)
            pfile.method = matches.group(2)
            if(pfile.url == None or pfile.method == None):
                raise Exception()
            log.debug('captured url %s', pfile.url)
            log.debug('captured method %s', pfile.method)
        except Exception as error:
            raise Exception('Cannot find method and url')

    def read_file(self, filePath):
        log.info('reading file %s', filePath)
        return open(filePath, 'r').read()
    

    def get_content_for(self, text, tag, defaultValue=None):
        regex = r"\[" + tag +"\]\s((.|\n|\r\n)*?)\["
        matches = re.search(regex, text, re.MULTILINE)
        if matches:
            content = matches.group(1)
            log.debug('tag content found in between for  \n[%s]\n%s\n', tag, content)
            return content
        
        regex = r"\["+tag+"\]\s((.|\n|\r\n)*)"
        matches = re.search(regex, text, re.MULTILINE)
        if matches:
            content = matches.group(1)
            log.debug('tag content found end for \n[%s]\n%s\n', tag, content)
            return content
        return defaultValue
    
file_processor = FileProcessor()