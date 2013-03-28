# coding=utf-8

'''
Created on Oct 3, 2012

@author: changlei
@email: changlei.abc@gmail.com
'''
import re
import log
import time
import random
import urllib2
from patent import Patent

class Parser(object):

    def __init__(self, content=""):
        '''
        Constructor
        '''
        self.content = content
        self.logger = log.LOG().getlogger()
        self.base_url = "http://www.soopat.com"
        
    def __get_patent_href(self):
        regex = u"<h2 class=\"PatentTypeBlock\">[\s\S]*?<a href='(.*?)'[\s\S]*?</h2>"
        return  re.findall(regex, self.content)

    def __get_page(self, url):
        res = urllib2.urlopen(url)
        html = res.read()
        return unicode(html, 'utf-8','ignore')
    
    def __get_patent_id(self, url):
        url = url.strip()
        return url[url.rfind("/")+1:]
    
    def __parse_item(self, regex, page_content):
        item = ""
        res = re.findall(regex, page_content)
        if len(res) > 0:
            item = res[0].strip()
        return item
    
    def __parse_title(self, page_content):
        regex = u"<h1>([\s\S]*?)<div"
        return self.__parse_item(regex, page_content)
    
    def __parse_state(self, page_content):
        regex = u"<h1>[\s\S]*?>([\s\S]*?)</div>"
        return self.__parse_item(regex, page_content)
    
    def __parse_abstract(self, page_content):
        regex = u"<b class=\"black\">摘要：</b>([\s\S]*?)</td>"
        return self.__parse_item(regex, page_content)

    def __parse_applier(self, page_content):
        regex = u"<b class=\"black\">申请人：</b>[\s\S]*?>([\s\S]*?)</a>"
        return self.__parse_item(regex, page_content)
    
    def __parse_author(self, page_content):
        regex = u"<b class=\"black\">发明.*</b>[\s\S]*?>([\s\S]*?)</a>"
        #regex = u"<b class=\"black\">发明(设计)人：</b>[\s\S]*?>([\s\S]*?)</a>"
        return self.__parse_item(regex, page_content)
    
    def __parse_author_address(self, page_content):
        regex = u"<b class=\"black\">地址：</b>([\s\S]*?)</td>"
        return self.__parse_item(regex, page_content)
    
    def __parse_notes(self, page_content):
        regex = u"<i>申请号：(.*?) 申请日"
        return self.__parse_item(regex, page_content)
    
    def __parse_date(self, page_content):
        regex = u">公开日[\s\S]*?>&nbsp;(.*?)</td>"
        return self.__parse_item(regex, page_content)
    
    def __parse_download_url(self, patent_id):
        url = "http://www.soopat.com/Home/DownloadChoice/%s" % patent_id
        page_content = self.__get_page(url)
        regex = u"<a href=\"(.*?)\?Server=\" target=\"_blank\">联通线路下载</a>"
        return self.__parse_item(regex, page_content)
    
    def get_patent_info(self, url):
        patent_id = self.__get_patent_id(url)
        
        page_content = self.__get_page(url)
        title = self.__parse_title(page_content)
        abstract = self.__parse_abstract(page_content)
        applier = self.__parse_applier(page_content)
        author = self.__parse_author(page_content)
        author_address = self.__parse_author_address(page_content)
        notes = self.__parse_notes(page_content)
        date = self.__parse_date(page_content)
        download_url = self.base_url + self.__parse_download_url(patent_id)
        state = self.__parse_state(page_content)
        
        author = author.replace("(", "").replace(")", "")
        patent = Patent(title, applier, author, date, abstract, url, download_url, author_address, notes, state)
        self.logger.info("parse patent ok, content is %s" % patent.to_dict())
        return patent
            
    def get_patents(self):
        patents = []
        hrefs = self.__get_patent_href()
        for href in hrefs:
            sleep_seconds = random.randint(5, 20)
            self.logger.info("sleep for %s seconds" % sleep_seconds)
            time.sleep(sleep_seconds)
            patent_info = self.get_patent_info(self.base_url + href)
            patents.append(patent_info)
        return patents
            
if __name__ == '__main__':
    parser = Parser()
    url = "http://www.soopat.com/Patent/200810052954"
    patent_info = parser.get_patent_info(url)
    print patent_info.to_ne()
    
