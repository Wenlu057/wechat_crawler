#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from urlGenerator import UrlGenerator
from httpRequestHandler import HttpRequestHandler
# from cookieManager import WechatCache
from htmlParser import HtmlParser
from const import CrawlerConst
import time

if len(sys.argv) < 2:
    print('No Official Account Specified.')
    sys.exit(1)


# ws_cache = WechatCache()
# gzh_name = '大纽约吃货小分队'


class SingleGzhCrawler(object):
    def __init__(self):
        self.gzh_name = sys.argv[1]
        self.request_handler = HttpRequestHandler()

    def __get_first_gzh_from_result_list(self):
        url_gzh_list = UrlGenerator.gen_search_article_url(self.gzh_name)
        print(url_gzh_list)
        res_gzh_list, success_flag = self.request_handler.get_sogou_response_content(url_gzh_list)
        return res_gzh_list, success_flag

    def __get_gzh_articles_dict(self, url_profile):
        res_gzh_profile, success_flag = self.request_handler.get_wechat_response_content(url_profile,
                                                                           UrlGenerator.gen_search_article_url(
                                                                               self.gzh_name,
                                                                               search_type=2))
        return res_gzh_profile, success_flag

    def __get_gzh_article(self, url_content):
        resp_gzh_article, success_flag = self.request_handler.get_wechat_response_content(url_content)
        return resp_gzh_article, success_flag

    def start_crawler(self):
        res_gzh_list, sogou_request_flag = self.__get_first_gzh_from_result_list()
        if sogou_request_flag == CrawlerConst.program_output_code.REQUEST_BLOCKED:
            return sogou_request_flag
        url_profile, first_gzh_name = HtmlParser.parse_gzh_list_html(res_gzh_list)
        if first_gzh_name != self.gzh_name:
            # print("找不到指定的公众号！请重新确认此公众号是否存在。")
            return CrawlerConst.program_output_code.OTHER_ERROR
        res_gzh_profile, wechat_return_flag = self.__get_gzh_articles_dict(url_profile)
        if wechat_return_flag == CrawlerConst.program_output_code.REQUEST_BLOCKED:
            return wechat_return_flag
        articles = HtmlParser.parse_history_article_list_html(res_gzh_profile)
        for article in articles:
            url_content = article['content_url']
            print(url_content)
            res_gzh_article, wechat_request_flag = self.__get_gzh_article(url_content)
            if wechat_request_flag == CrawlerConst.program_output_code.REQUEST_BLOCKED:
                return wechat_request_flag
            save_res = HtmlParser.parse_history_article_html(res_gzh_article, self.gzh_name)
            if save_res == CrawlerConst.program_output_code.SAVE_FAILURE:
                return save_res
        return CrawlerConst.program_output_code.SUCCESS


if __name__ == "__main__":
    crawler = SingleGzhCrawler()
    output_res = crawler.start_crawler()
    print(output_res)
    # for i in range(200):
    #     url_gzh_list = UrlGenerator.gen_search_article_url(crawler.gzh_name)
    #     res_gzh_list, success_flag = crawler.request_handler.get_sogou_response_content(url_gzh_list)
    #     print(i)
        # time.sleep(5)
