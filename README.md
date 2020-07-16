## 爬虫练习

### 程序说明

编写两个线程对象分别维护两个队列，一个用于保存URL及深度，另一个负责将爬取到的内容存储至本地，
主函数在spider.py中负责初始化两个任务队列。

### 使用说明
终端输入
<code>python3 spider.py -u http://www.yingjiesheng.com -d 2</code>
将自动爬取不同深度的网页及链接（默认为2），输出内容保存至"Downloads"文件夹下，
格式为"A\[B]"，
A表示HTML的编号，B表示保存页面的URL深度。

### 参考链接
>1. https://www.metachris.com/2016/04/python-threadpool/
>2. https://www.ibm.com/developerworks/cn/aix/library/au-threadingpython/?ca=drs-tp3008#resources
>3. https://github.com/littlethunder/knowsecSpider2
