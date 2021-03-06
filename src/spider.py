# coding=utf-8

'''
Created on Oct 3, 2012

@author: changlei
@email: changlei.abc@gmail.com
'''

import re
import log
import urllib
import urllib2 as url

class SoopatSpider(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = log.LOG().getlogger()
    
    def soopat_search(self, keyword, PatentIndex=0):
        p = {'SearchWord': keyword, 'PatentIndex': PatentIndex}
        res = url.urlopen("http://www.soopat.com/Home/Result?%s" % (urllib.urlencode(p)))
        html = res.read()
        return unicode(html, 'utf-8','ignore')
    
    def get_search_result_num(self, content):
        sum = 0
        regex = u"<p class=\"right\"><b>([1-9]\d*)</b>.*</p>"
        res = re.findall(regex, content)
        if len(res) == 1:
            sum = int(res[0])
            logstr = "get sum of result: %s" % sum
            self.logger.info(logstr)
        else:
            msg = "cannot get search result"
            self.logger.error(msg)
            raise ValueError(msg)
        return sum

if __name__ == '__main__':
    soopat = SoopatSpider()
    content = soopat.soopat_search("负载均衡")
    sum = soopat.get_search_result_num(content)

    print sum
