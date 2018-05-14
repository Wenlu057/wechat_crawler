import requests
# from securityCodeHandler import SecurityCodeHandler
from cookieManager import SnuidQueueManager
from const import CrawlerConst


class HttpRequestHandler(object):

    def __init__(self):
        # self.ws_cache = ws_cache
        # self.security_code_handler = None
        self.snuid_queue = SnuidQueueManager()  # 初始化snuid queue，加10个snuid进queue

    def get_sogou_response_content(self, url, referer=None):
        """
        :param url: URL for the new Request object.
        :param referer:
        :return: Response object

        给定一个url， 发送http request返回response

        """
        success_flag = CrawlerConst.program_output_code.SUCCESS
        session = requests.session()
        snuid = self.__get_snuid_from_queue(self.snuid_queue)  # 从snuid queue中拿到头一个snuid
        resp = session.get(url, headers=self.__set_sogou_cookies(snuid))
        # 处理验证码的问题
        while 'antispider' in resp.url or '请输入验证码' in resp.text:
            if self.snuid_queue.get_queue().empty() is not True:
                snuid = self.__get_snuid_from_queue(self.snuid_queue)  # 最近拿到的snuid不好使了，重新拿一个
                resp = session.get(url, headers=self.__set_sogou_cookies(snuid))
            else:
                print("所有cookie值都已用完！！")
                self.snuid_queue.update_queue()
                snuid = self.__get_snuid_from_queue(self.snuid_queue)  # 最近拿到的snuid不好使了，重新拿一个
                resp = session.get(url, headers=self.__set_sogou_cookies(snuid))
                if 'antispider' in resp.url or '请输入验证码' in resp.text:
                    break

                # success_flag = CrawlerConst.program_output_code.REQUEST_BLOCKED
                # break
            # else:
            #     print("Bang！你触发了微信的验证码机制")
            """
            下面加了注释的代码，解决出现验证码的问题，用手动打码的机制来更新snuid
            """
            # for i in range(1):
            #     try:
            #         self.security_code_handler = SecurityCodeHandler(url, resp, session, self.ws_cache)
            #         self.security_code_handler.handle_sogou_security_code()
            #         break
            #     except (RuntimeError, TypeError, NameError):
            #         pass
            # resp = session.get(url, headers=self.__set_cookie(referer=referer))
        self.snuid_queue.put_into_queue(snuid)
        return resp, success_flag

    def get_wechat_response_content(self, url, referer=None):
        """
        :param url: URL for the new Request object.
        :param referer:
        :return: Response object

        给定一个url， 发送http request返回response

        """
        success_flag = CrawlerConst.program_output_code.SUCCESS
        session = requests.session()
        _headers = {'Referer': referer}
        resp = session.get(url, headers=_headers)
        # 处理验证码的问题
        if 'antispider' in resp.url or '请输入验证码' in resp.text:
            print("Bang！你触发了微信的验证码机制")
            success_flag = CrawlerConst.program_output_code.REQUEST_BLOCKED

        return resp, success_flag

    @staticmethod
    def get_response_content_without_header(url):
        res = requests.get(url)
        return res

    @staticmethod
    def get_pics_response_content(url, stream=True):
        return requests.get(url, stream=stream)

    @staticmethod
    def __get_snuid_from_queue(snuid_queue):
        snuid = ''
        if snuid_queue.get_queue().empty() is not True:
            snuid = snuid_queue.get_queue().get()
        return snuid

    @staticmethod
    def __set_sogou_cookies(snuid, referer=None, ):
        if snuid != '':
            _headers = {'Cookie': 'ABTEST={};IPLOC={};SUID={};PHPSESSID={};SUIR={};SNUID={};SUIR={};SUV={};sct=1'.format(
                CrawlerConst.cookie_value.ABTEST, CrawlerConst.cookie_value.IPLOC, CrawlerConst.cookie_value.SUID,
                CrawlerConst.cookie_value.PHPSESSID, CrawlerConst.cookie_value.SUIR, snuid, CrawlerConst.cookie_value.SUIR,
                CrawlerConst.cookie_value.SUV)}
        # 68次之后跳验证码
        # _headers = {
        #     'Cookie': 'ABTEST=6|1522793716|v1; JSESSIONID=aaanmwSYG5DB5buEbxQiw; PHPSESSID=hqd94hian8h9g5g5a7rek22pd7; SUID=43BBE5482930990A000000005AC4E53A; IPLOC=US; SUIR=1522853603; SUV=1522853622627738; SNUID=B45858412013940A000000005AC540A3; sct=1'}
        if referer is not None:
            _headers['Referer'] = referer
        return _headers
