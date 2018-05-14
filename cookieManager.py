# from werkzeug.contrib.cache import FileSystemCache
import requests
import re
from const import CrawlerConst
import queue
import random


# class WechatCache(FileSystemCache):
#     """
#     基于文件的缓存
#
#     """
#
#     def __init__(self, cache_dir='/tmp/wechatsogou-cache', default_timeout=300):
#         """初始化
#
#         cache_dir是缓存目录
#         """
#         super(WechatCache, self).__init__(cache_dir, default_timeout)


class CookieSnuidGenerator(object):

    @staticmethod
    def generate_from_url():
        url = "https://www.sogou.com/web?query=333&_asf=www.sogou.com&_ast=1488955851&w=01019900&p=40040100&ie=utf8" \
              "&from=index-nologin "
        headers = {"Cookie": "IPLOC={};SUIR={};SUV={};ABTEST={};SUID={};PHPSESSID={};".format(
                CrawlerConst.cookie_value.IPLOC,
                CrawlerConst.cookie_value.SUIR, CrawlerConst.cookie_value.SUV,
                CrawlerConst.cookie_value.ABTEST, CrawlerConst.cookie_value.SUID,
                CrawlerConst.cookie_value.PHPSESSID)
        }
        f = requests.head(url, headers=headers).headers
        res = re.findall(r"SNUID=(.*?);", f['Set-Cookie'])
        if res != '':
            return res[0]
        else:
            return -1
    """下面这个不好使"""
    @staticmethod
    def generate_from_antispider():
        """
        http://www.sogou.com/antispider/util/seccode.php?tc=1488958062 验证码地址
        """
        '''
        http://www.sogou.com/antispider/?from=%2fweb%3Fquery%3d152512wqe%26ie%3dutf8%26_ast%3d1488957312%26_asf%3dnull%26w%3d01029901%26p%3d40040100%26dp%3d1%26cid%3d%26cid%3d%26sut%3d578%26sst0%3d1488957299160%26lkt%3d3%2C1488957298718%2C1488957298893
        访问这个url，然后填写验证码，发送以后就是以下的包内容，可以获取SNUID。
        '''
        unlock_url = 'http://weixin.sogou.com/antispider/thank.php'
        data = {
            'c': '88DDX3',
            'r': '%2Fweb%3Fquery%3D152512wqe%26ie%3Dutf8%26_ast%3D1488957312%26_asf%3Dnull%26w%3D01029901%26p%3D40040100'
                 '%26dp%3D1%26cid%3D%26cid%3D%26sut%3D578%26sst0%3D1488957299160%26lkt%3D3%2C1488957298718'
                 '%2C1488957298893',
            'v': 5
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.sogou.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'IPLOC={}; SUIR={}; SUV={}; ABTEST={};SUID={}; browerV=3; osV=2; PHPSESSID={};sst0=160; sct=3; SNUID={}; seccodeRight={}; successCount= {}; ld={}'.format(
                CrawlerConst.cookie_value.IPLOC, CrawlerConst.cookie_value.SUIR, CrawlerConst.cookie_value.SUV,
                CrawlerConst.cookie_value.ABTEST, CrawlerConst.cookie_value.SUID, CrawlerConst.cookie_value.PHPSESSID,
                CrawlerConst.cookie_value.SNUID, CrawlerConst.cookie_value.seccodeRight, CrawlerConst.cookie_value.successCount,
                CrawlerConst.cookie_value.ld
            )
        }
        r_unlock = requests.post(unlock_url, data=data, headers=headers).json()
        if r_unlock['code'] == 0:
            return r_unlock['id']
        else:
            return -1


class SnuidQueueManager(object):
    def __init__(self):
        self.q = queue.Queue(10)
        self.initialize_queue()

    def initialize_queue(self):
        """
        指定queue的大小，将snuid不断的插入进queue
        """
        for i in range(2):
            Snuid = CookieSnuidGenerator.generate_from_url()
            # Snuid = random.choice([CookieSnuidGenerator.generate_from_url(), CookieSnuidGenerator.generate_from_antispider()])
            if Snuid != -1:
                self.q.put(Snuid)

    def update_queue(self):
        for i in range(2):
            snuid = CookieSnuidGenerator.generate_from_url()
            if snuid != -1:
                self.q.put(snuid)

    def get_queue(self):
        return self.q

    def put_into_queue(self, snuid):
        self.q.put(snuid)

    def get_queue_size(self):
        return self.q.qsize()