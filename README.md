soopat_downloader
=================

www.soopat.com 是一个免费的专利搜索和下载引擎，soopat_downloader是python写的一个批量解析并下载专利文献的工具。

使用方法：

python main.py --help
Usage: main.py [options] arg

Options:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword=KEYWORD
                        the keyword to be searched
  -u USERNAME, --username=USERNAME
                        username to login website
  -p PASSWORD, --pasword=PASSWORD
                        password to login website
                        
该工具默认下载最多10页的搜索结果

example:                        
使用方法： python main.py -k 负载均衡 -u xxxxx -p *****
输出结果： 负载均衡.txt   ----> noteexpress 样式的题录文件，可直接导入到专业文献管理软件noteexpress中
           ****.pdf  若干专利文献的pdf

contact me: mail:       changlei.abc@gmail.com  
            sina weibo: http://weibo.com/irontiger88

enjoy!

                        
                        