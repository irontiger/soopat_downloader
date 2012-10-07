# coding=utf-8

'''
Created on Oct 3, 2012

@author: changlei
@email: changlei.abc@gmail.com
'''

import log
import sys
import time
import random
import codecs
from spider import SoopatSpider
from parser import Parser
from downloader import Downloader
from optparse import OptionParser

logfile = 'soopt_downloader.log'
logger = log.LOG(logfile).getlogger()

def get_patent_page_num(search_result_num, default_page_num = 10):
    page_size = 10
    real_page_num =  (search_result_num + page_size/2)/10 
    
    if real_page_num < default_page_num:
        return real_page_num
    else:
        return default_page_num
    
def get_page_patents(keyword, page_num):
    patent_index = page_num * 10
    spider = SoopatSpider()
    content = spider.soopat_search(keyword, patent_index)
    parser = Parser(content)
    logger.info("get page %s patents ok" % page_num) 
    return parser.get_patents()

def get_all_page_patents(keyword):
    all_patents = []
    logger.info("start to get patents, keyword %s" % keyword)
    spider = SoopatSpider()
    content = spider.soopat_search(keyword)
    search_result_num = spider.get_search_result_num(content)
    page_num = get_patent_page_num(search_result_num)
    for i in range(page_num):
        sleep_seconds = random.randint(5, 20)
        logger.info("sleep for %s seconds" % sleep_seconds)
        time.sleep(sleep_seconds)
        patents = get_page_patents(keyword, i)
        for patent in patents:
            all_patents.append(patent)
    logger.info("get %s patents, keyword %s" % (len(all_patents), keyword))
    logger.info("end to get patents, keyword %s" % keyword)
    return all_patents

def save_patents_to_ne(patents, file_name):
    is_save_ok = False
    try:
        f = codecs.open(file_name, "w", "utf-8")
        for patent in patents:
            f.write(patent.to_ne())
            f.write("\n")
        is_save_ok = True
    except Exception, e:
        logger.info(e)
        raise Exception
    finally:
        f.close( )
        logger.info("save patents to ne %s" % is_save_ok)
        return is_save_ok
    
def download_patents(patents, username, password):
    dler = Downloader(patents)
    dler.download_patents(username, password)
        
if __name__ == '__main__':
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage)
    parser.add_option("-k", "--keyword", dest="keyword", default="负载均衡",
                      help="the keyword to be searched")
    parser.add_option("-u", "--username", dest="username",
                      help="username to login website")
    parser.add_option("-p", "--pasword", dest="password",
                      help="password to login website")

    (options, args) = parser.parse_args()
    keyword = options.keyword
    username = options.username
    password = options.password
    
    if not (username and password):
        print "please input username and password"
        parser.print_help()
        sys.exit(1)
    
    patents = get_all_page_patents(keyword)
    
    print "start to save patents to noteexpress style"
    file_name = keyword + ".txt"
    save_patents_to_ne(patents, file_name)
    print "end of save patents to noteexpress style"
    
    print "start to download patents"
    download_patents(patents, username, password)
    print "end of download patents"
    
