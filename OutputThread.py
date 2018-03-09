import os
from threading import Thread


class OutputThread(Thread):
    def __init__(self, content_queue):
        Thread.__init__(self)
        self.content_queue = content_queue

    def run(self):
        """将内容队列取出并保存到本地"""
        while True:
            # 从content队列取出内容
            content_id, depth, content = self.content_queue.get()

            # 将id, 深度，content保存至本地HTML
            self._save_to_html(str(content_id) + '[' + str(depth) + ']', content)

            self.content_queue.task_done()

    @staticmethod
    def _save_to_html(filename, file):
        DEST_DIR = './Downloads/'
        path = os.path.join(DEST_DIR, filename+'.html')
        with open(path, 'wb') as f:
            if file:
                f.write(file)