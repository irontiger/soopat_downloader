# coding=utf-8

'''
Created on Oct 4, 2012

@author: changlei
@email: changlei.abc@gmail.com
'''

class Patent(object):

    def __init__(self, title, applier, author, date, abstract, url, download_url, author_address = None, notes = None, state = None):
        self.reference_type = "Patent"
        self.title = title
        self.applier = applier
        self.author = author
        self.date = date
        self.abstract = abstract
        self.url = url
        self.download_url = download_url
        self.author_address = author_address
        self.notes = notes
        self.state = state
    
    def to_dict(self):
        dct = {}
        for (key, val) in self.__dict__.items():
            dct[key] = val
        return dct
        
    def to_ne(self):
        '''
            to noteexpress
            
            {Reference Type}: Patent
            {Title}: 复合一体化托辊支架
            {Author}: 发明人
            {Subsidiary Author}: 申请人
            {Date}: 2012-08-08
            {Abstract}: 本外观设计的产品名称为复合一体化托辊支架。本外观设计的产品是用于皮带输送机的安装。本外观设计的设计要点在于产品的形状。指定的图片为主视图。主视图和后视图相同,省略后视图；左视图和右视图相同,省略右视图。
            {URL}: http://d.g.wanfangdata.com.cn/Patent_CN201110047724.8.aspx
            {Author Address}: 443000 湖北省宜昌市猇亭区正大路65号
            {Notes}: CN302029643S
            {Year}: 2012
        '''
        ne = ""
        ne = ne + "".join(("{Reference Type}: ", self.reference_type, "\r\n"))
        ne = ne + "".join(("{Title}: ", self.title, "\r\n"))
        ne = ne + "".join(("{Author}: ", self.author.replace(' ',''), "\r\n"))
        ne = ne + "".join(("{Subsidiary Author}: ", self.applier.replace('(','').replace(')',''), "\r\n"))
        ne = ne + "".join(("{Date}: ", self.date, "\r\n"))
        ne = ne + "".join(("{Abstract}: ", self.abstract, "\r\n"))
        ne = ne + "".join(("{URL}: ", self.url, u"  详细地址", "\r\n"))
        ne = ne + "".join((self.download_url, u"  下载地址", "\r\n"))
        ne = ne + "".join(("{Author Address}: ", self.author_address, "\r\n"))
        ne = ne + "".join(("{Notes}: ", self.notes, "\r\n"))
        ne = ne + "".join(("{Year}: ", self.date[:4], "\r\n"))
        ne = ne + "".join(("{Custom 1}: ", self.state, "\r\n"))
        
        return ne
