# coding=utf-8

'''
Created on Oct 3, 2012

@author: changlei
@email: changlei.abc@gmail.com
'''

import os
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
from argparse import ArgumentParser

__DESCRIPTION__ = "soopat tool, to parse soopat content and write to noteexpress style"
__VERSION__ = 0.2
__CONTACT__ = 'For more information, please contact changlei.abc@gmail.com'

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

def get_url_patents(url):
    all_patents = []
    parser = Parser()
    
    try:
        pat = parser.get_patent_info(url)
        all_patents.append(pat)
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
                pat = Patent(js["title"], js["applier"], js["author"], js["date"], js["abstract"], 
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

def rename_patents(patents_dir):

    def is_need_rename(filename):
        is_need = False

        if len(filename) > 4 and filename[-4:].lower() == '.pdf':
            names = filename.split('-')
            if len(names) == 3:
                is_need = True

        return is_need

    files = os.listdir(patents_dir)
    for f in files:
        is_need = is_need_rename(f)
        if is_need:
            logger.info("%s/%s need to be renamed" % (patents_dir, f)) 
            names = f.split('-')
            patent_id = names[0]
            patent_url = "http://www.soopat.com/Patent/%s" % patent_id 
            patents = get_url_patents(patent_url)
            if len(patents) == 1:
                patent = patents[0] 

                new_patent_name =  "%s-%s%s" % (patent_id, patent.title, '.pdf')
                old_full_name = "%s/%s" % (patents_dir, f)
                new_full_name = "%s/%s" % (patents_dir, new_patent_name)
                msg = "rename %s to %s" % (old_full_name.decode('utf-8'), new_full_name)
                print msg
                logger.info(msg)
                os.rename(old_full_name, new_full_name)

HELP_INFO = dict(
                 input = 'the output of parse result file',
                 parse_input = 'keyword or patent url. when url, must contain word Patent ',
                 parse_output = 'write parse result to file',
                 is_write2ne = 'write to noteexpress or not, default is True',
                 write2ne_output = 'optional, write to noteexpress style. if null, use input as output file name',
                 download_output = 'optional, download failed patents',
                 username = 'username to login website',
                 password = 'password to login website',
                 directory = 'dir path which include patent pdfs',
                 )

def parse_command_line():
    parser = ArgumentParser(description=__DESCRIPTION__, epilog=__CONTACT__)
    subparsers = parser.add_subparsers()

    parse_parser = subparsers.add_parser('parse', help='parse soopat content')
    parse_parser.add_argument('-i', dest='input', default='', help=HELP_INFO['parse_input'])
    parse_parser.add_argument('-o', dest='output', default='', help=HELP_INFO['parse_output'])
    parse_parser.add_argument('-w', dest='iswrite2ne', default=True, help=HELP_INFO['is_write2ne'])

    write2ne_parser = subparsers.add_parser('write2ne', help='write to noteexpress style')
    write2ne_parser.add_argument('-i', dest='input', default='', help=HELP_INFO['input'])
    write2ne_parser.add_argument('-o', dest='output', default='', help=HELP_INFO['write2ne_output'])

    download_parser = subparsers.add_parser('download', help='download patent files')
    download_parser.add_argument('-i', dest='input', default='', help=HELP_INFO['input'])
    download_parser.add_argument('-u', dest='username', default='', help=HELP_INFO['username'])
    download_parser.add_argument('-p', dest='password', default='', help=HELP_INFO['password'])
    download_parser.add_argument('-o', dest='output', default='', help=HELP_INFO['download_output'])

    rename_parser = subparsers.add_parser('rename', help='rename patent pdf file')
    rename_parser.add_argument('-d', dest='dir', default='', help=HELP_INFO['directory'])

    return parser.parse_args(sys.argv[1:]), parser

def main():
    args, parser = parse_command_line()

    def sys_exit(parser):
        parser.print_help()
        sys.exit(1)

    try:
        if sys.argv[1] == 'parse':
            if not args.input:
                print "must specify -i"
                sys_exit(parser)
            if not args.output:
                print "must specify -o"
                sys_exit(parser)

            patents = []
            print "start to parse patents"
            if args.input.find('Patent') >= 0:
                patents = get_url_patents(args.input)
            else:
                patents = get_all_page_patents(args.input)
            print "end of parse patents"
            
            file_name = args.output.replace(".", "_")
            pat_name = file_name + ".pat"
            is_success = write_patents(patents, pat_name)
            if is_success:
                print "write patents to file %s success" % file_name
            else:
                print "write patents failed"
                sys.exit(1)

            if args.iswrite2ne:
                ne_name = file_name + ".ne"
                print "start to save patents to noteexpress style"
                save_patents_to_ne(patents, ne_name)
                print "end of save patents to noteexpress style"

        elif sys.argv[1] == 'write2ne':
            if not args.input:
                print "must specify -i"
                sys_exit(parser)

            if args.output:
                file_name = args.output.replace(".", "_") + ".ne"
            else:
                base = os.path.basename(args.input)
                if base.find(".pat") > 0:
                    base = base[0:base.find(".pat")]
                file_name = base.replace(".", "_") + ".ne"

            patents = read_patents(args.input)
            print "start to save patents to noteexpress style"
            save_patents_to_ne(patents, file_name)
            print "end of save patents to noteexpress style"

        elif sys.argv[1] == 'download':
            if not args.input:
                print "must specify -i"
                sys_exit(parser)
            if not args.username:
                print "must specify -u"
                sys_exit(parser)
            if not args.password:
                print "must specify -p"
                sys_exit(parser)

            if args.output:
                file_name = args.output.replace(".", "_") + "_failed.pat"
            else:
                base = os.path.basename(args.input)
                if base.find(".pat") > 0:
                    base = base[0:base.find(".pat")]
                file_name = base.replace(".", "_") + "_failed.pat"
            patents = read_patents(input)
            
            print "start to download patents"
            failed_patents = download_patents(patents, username, password)
            if failed_patents:
                print "write download failed patents to file %s" % file_name
                is_success = write_patents(failed_patents, file_name)
                print "end of download, and exist download failed patents"
            else:
                print "download success"

        elif sys.argv[1] == 'rename':
            if not os.path.isdir(args.dir):
                print "must specify -d"
                sys_exit(parser)

            print "start to rename patents"
            rename_patents(args.dir)
            print "end of rename patents"
                
        else:
            sys_exit(parser)

    except Exception, e:
        print "exception:%s" % e
        
if __name__ == '__main__':
    main()
