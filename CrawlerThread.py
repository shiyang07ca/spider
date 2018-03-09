import re
from threading import Thread

import requests
import bs4

class CrawlerThread(Thread):
    """从URL线程队列取出URL，将返回的响应存入内容队列"""
    def __init__(self, url_queue, content_queue):
        Thread.__init__(self)
        self.url_queue = url_queue  # URL队列
        self.content_queue = content_queue  # 内容队列
        self.content_id = 1  # 内容编号，用于给文件命名
        self.urls = set()  # 用于链接去重

    def run(self):
        while True:
            # 从url队列提取URL及深度，并请求页面内容
            url, depth = self.url_queue.get()
            content = self._request_data(url)

            # 将id,content放入队列
            self.content_queue.put((self.content_id, depth, content))
            self.content_id += 1

            # 如果深度大于零，提取页面链接并存入url_queue（深度为零说明到达最后一层，不再更新链接）
            if depth > 0:
                for link in self._extract_all_links(content):
                    if link not in self.urls:
                        self.urls.add(link)
                        self.url_queue.put((link, depth-1))

            self.url_queue.task_done()

    @staticmethod
    def _request_data(url):
        '''返回指定URL响应对象'''
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,\
            application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686)\
            AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/35.0.1916.153 Safari/537.36',
             'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }
        if url is None:
            raise RuntimeWarning('url is None')
        try:
            resp = requests.get(url, headers=headers, timeout=2)
        except Exception as e:
            print(e)
        else:
            if resp.status_code != 200:
                resp.raise_for_status()
            return resp.content
        return None

    @staticmethod
    def _extract_all_links(content):
        '''返回页面内所有连接'''
        bs = bs4.BeautifulSoup(content, 'html.parser')
        links = []
        for item in bs.find_all('a', attrs={"href":re.compile(r'^(https?|www).*$')}):
            links.append(item.attrs['href'])
        # 将新的链接保存起来（测试用）
        with open('links.txt', 'a+') as f:
            for l in links:
                f.writelines(l)
                f.write('\n')
            f.write('*' * 20)
        return links