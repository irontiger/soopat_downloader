#encoding=utf-8

'''
Created on Oct 5, 2012

@author: changlei
'''
import log
import time
import random
import urllib
import urllib2
import cookielib

class Downloader(object):

    def __init__(self, patents):
        self.patents = patents
        self.logger = log.LOG().getlogger()
    
    def get_opener(self, username, password):
        rtn_opener = None
        login_page = "http://t.soopat.com/index.php?mod=login&code=dologin"
        try:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
            post_data = {
                'FORMHASH': '0cbba408b58f6291',
                'username': username,
                'loginType':'share',
                'return_url':'http://www.soopat.com/Home/Index',
                'password': password
            }
            opener.open(login_page, urllib.urlencode(post_data))
            rtn_opener = opener
        except Exception,e:
            self.logger.error(str(e))
            raise Exception(str(e))
        return rtn_opener
        
    def download_patents(self, username, password):
        opener = self.get_opener(username, password)
        if not opener:
            self.logger.error("opener is None")
        else:
            index = 0
            for patent in self.patents:
                self.logger.info("start to download %s in %s patents, title: %s" % (index, len(self.patents), self.title))
                sleep_seconds = random.randint(5, 20)
                self.logger.info("sleep for %s seconds" % sleep_seconds)
                time.sleep(sleep_seconds)
                op = opener.open(patent.download_url)
                data = op.read()
                with open( patent.title+".pdf", "wb") as f:
                    f.write(data)
                self.logger.info("end of download %s in %s patents, title: %s" % (index, len(self.patents), self.title))
                index += 1

if __name__ == '__main__':
    dler = Downloader([])

