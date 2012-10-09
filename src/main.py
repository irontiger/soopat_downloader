# coding=utf-8

'''
Created on Oct 3, 2012

@author: changlei
@email: changlei.abc@gmail.com
'''

import log
import sys
import time
import json
import random
import codecs
from patent import Patent
from spider import SoopatSpider
from parser import Parser
from downloader import Downloader
from optparse import OptionParser

logfile = 'soopt_downloader.log'
logger = log.LOG(logfile).getlogger()

def get_patent_page_num(search_result_num, default_page_num = 1):
    page_size = 10
    real_page_num =  (search_result_num + page_size/2)/page_size 
    
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

def get_url_patents(urlfile):
    all_patents = []
    parser = Parser()
    
    try:
        with open(urlfile, "r") as f:
            line = f.readline()
            pat = parser.get_patent_info(line)
            all_patents.append(pat)
            line = f.readline()
    except Exception, e:
        logger.error("get url patents from file get exception, msg %s" % str(e))
    
    return all_patents

def write_patents(patents, filename):
    is_success = False
    
    try:
        with open(filename, "w") as f:
            for pat in patents:
                f.write(json.dumps(pat.to_dict()))
                f.write("\n")
        f.close()
        is_success = True
    except Exception, e:
        logger.error("write patents to file failed, msg %s" % str(e))
    
    return is_success

def read_patents(filename):
    patents = []
    try:
        with open(filename, "r") as f:
            line = f.readline()
            while line:
                js = json.loads(line, "utf-8")
                pat = Patent(js["title"], js["author"], js["date"], js["abstract"], 
                             js["url"], js["download_url"], js["author_address"], js["notes"], js["state"])
                
                patents.append(pat)
                line = f.readline()
    except Exception, e:
        logger.error("read patents file get exception, msg %s" % str(e))
            
    return patents

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
    dler = Downloader(username, password)
    dler.download_patents(patents)
        
if __name__ == '__main__':
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage)
    parser.add_option("-c", "--cmd", dest="cmd", default="parse",
                  help="parse|download|write2ne")
    parser.add_option("-k", "--keyword", dest="keyword", default="负载均衡",
                      help="the keyword to be searched")
    parser.add_option("-i", "--input", dest="input",
                      help="for cmd parse: indicate url file to be parsed.        for cmd download/write2ne: indicate patents result file.")
    parser.add_option("-o", "--output", dest="output",
                      help="for cmd parse: indicate parse result to be parsed.    for cmd download: indicate download failed patents.  for cmd write2ne: indicate noteexpress style description")
    parser.add_option("-u", "--username", dest="username",
                      help="username to login website when download patents")
    parser.add_option("-p", "--pasword", dest="password",
                      help="password to login website when download patents")

    (options, args) = parser.parse_args()
    cmd = options.cmd
    keyword = options.keyword
    input = options.input
    output = options.output
    username = options.username
    password = options.password
        
    if cmd == "parse":
        if not (keyword or input):
            print "keyword or input, at least one must specifed"
            parser.print_help()
            sys.exit(1)
            
        if not output:
            print "output must specifed"
            parser.print_help()
            sys.exit(1)
            
        patents = []
        print "start to parse patents"
        if keyword:
            patents = get_all_page_patents(keyword)
        if input:
            patents = get_url_patents(input)
        print "end of parse patents"
        
        file_name = output.replace(".", "_") + ".pat"
        is_success = write_patents(patents, file_name)
        if is_success:
            print "write patents to file %s success" % file_name
        else:
            print "failed to get patents"
        
    elif cmd == "write2ne":
        if not(input and output):
            print "input and output must specifed"
            parser.print_help()
            sys.exit(1)
        
        patents = read_patents(input)
        file_name = output.replace(".", "_") + ".ne"
        
        print "start to save patents to noteexpress style"
        save_patents_to_ne(patents, file_name)
        print "end of save patents to noteexpress style"
    
    elif cmd == "download":
        if not(input and output):
            print "input and output must specifed"
            parser.print_help()
            sys.exit(1)
            
        if not (username and password):
            print "username and password must specifed"
            parser.print_help()
            sys.exit(1)
        
        patents = read_patents(input)
        file_name = output.replace(".", "_") + "_failed_download.pat"
        
        print "start to download patents"
        failed_patents = download_patents(patents, username, password)
        if failed_patents:
            print "write download failed patents to file %s" % file_name
            is_success = write_patents(patents, file_name)
            print "end of download, and exist download failed patents"
        else:
            print "download success"
            
    else:
        parser.print_help()
        sys.exit(1)
    
