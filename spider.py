#!/usr/bin/env python
'''
    Version: 0.1
'''

import time
import optparse
from queue import Queue

from CrawlerThread import CrawlerThread
from OutputThread import OutputThread


def parse_options():
    parser = optparse.OptionParser()

    parser.add_option("-u", "--url", dest="url", type="string")

    parser.add_option("-d", "--depth", dest="depth", type="int")

    options, _ = parser.parse_args()

    return options


# TODO: 编写主调度函数，封装该逻辑
def main(root_url, num_threads=10, depth=2):
    start = time.time()
    # 初始化两个任务队列，一个存储待爬取URL，一个用来存储待保存的内容
    url_queue = Queue()
    content_queue = Queue()

    for _ in range(num_threads):
        cr = CrawlerThread(url_queue, content_queue)
        cr.start()
    # 存入初始URL及深度的tuple
    url_queue.put((root_url, depth))
    for _ in range(num_threads):
        ot = OutputThread(content_queue)
        ot.start()

    # 阻塞线程直到任务完成
    try:
        url_queue.join()
        content_queue.join()
    except KeyboardInterrupt:
        print("Key Interrupt")
    else:
        print('****ALL DONE****')
    print("Elapsed Time: %s" % (time.time() - start))


if __name__ == "__main__":
    # root_url = "https://news.ycombinator.com/news"
    # root_url = "https://www.zhibo8.cc/"
    root_url = "http://www.yingjiesheng.com"
    options = parse_options()
    root_url = options.url or root_url
    depth = options.depth or 2

    main(root_url, depth=depth)
