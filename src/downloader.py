#encoding=utf-8

'''
Created on Oct 5, 2012

@author: changlei
@email: changlei.abc@gmail.com
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
            index = 1
            for patent in self.patents:
                self.logger.info("start to download %s in %s patents, title: %s" % (index, len(self.patents), patent.title))
                sleep_seconds = random.randint(5, 30)
                self.logger.info("sleep for %s seconds" % sleep_seconds)
                time.sleep(sleep_seconds)
                op = opener.open(patent.download_url)
                data = op.read()
                with open( patent.title+".pdf", "wb") as f:
                    f.write(data)
                self.logger.info("end of download %s in %s patents, title: %s" % (index, len(self.patents), patent.title))
                index += 1

if __name__ == '__main__':

    from patent import Patent
    
    title = "动态负载均衡系统"
    author = "北京天润融通科技有限公司"
    date = "2012-07-18"
    abstract = "本发明公开了一种动态负载均衡系统，该系统包括客户A的电话"
    url = "http://www.soopat.com/Patent/201210080259"
    download_url = "http://www.soopat.com/Home/DownloadRemote/837A885AB57D6A3903688CAEA88544BDDE2F65B6F3AC51ED.pdf"
    author_address = "100176 北京市大兴区亦庄经济技术开发区地盛北街1号北工大软件园18号楼5层"
    notes = "201210080259.2"
    
    pat = Patent(title, author, date, abstract, url, download_url, author_address, notes)
    dler = Downloader([pat])
    

