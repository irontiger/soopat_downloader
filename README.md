soopat_downloader
=================

<pre>
www.soopat.com 是一个免费的专利搜索和下载引擎，soopat_downloader是python写的一个批量解析并下载专利文献的工具。

使用方法：

python main.py --help
Usage: main.py [options] arg

Options:
  -h, --help            show this help message and exit
  -c CMD, --cmd=CMD     parse|download|write2ne
  -k KEYWORD, --keyword=KEYWORD
                        the keyword to be searched
  -i INPUT, --input=INPUT
                        for cmd parse: indicate url file to be parsed.
                        for cmd download/write2ne: indicate patents result
                        file.
  -o OUTPUT, --output=OUTPUT
                        for cmd parse: indicate parse result to be parsed.
                        for cmd download: indicate download failed patents.
                        for cmd write2ne: indicate noteexpress style
                        description
  -u USERNAME, --username=USERNAME
                        username to login website when download patents
  -p PASSWORD, --pasword=PASSWORD
                        password to login website when download patents
                        
该工具默认下载最多5页的搜索结果

example:
1. 解析网页
使用方法： python main.py  -c parse -k 健康检测 -o health  或者 python main.py  -c parse -i urlfile -o health
输出结果： health.pat                 ---->解析结果的数据文件，为 download/write2ne 的input数据来源

2. 下载文件
使用方法： python main.py  -c download -i health.pat -o health -u xxxxxxx -p *****
输出结果： ***.pdf                     ---->下载的pdf文件
           health_failed_download.pat  ---->下载失败的数据，可用于下一次下载的数据源

3. 生成note express 样式的题录
使用方法: python main.py  -c write2ne -i health.pat -o health
输出结果: health.ne                    ----->noteexpress样式的题录，可直接导入到专业文献管理软件noteexpress中

注意： 下载文件失败，主要是由于需要输入验证码，这个验证码比较难识别，有好的办法自动识别它的验证码，请联系我

contact me: mail:       changlei.abc@gmail.com  
            sina weibo: http://weibo.com/irontiger88

enjoy!

</pre>
                        
                        