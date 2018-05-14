import urllib.parse
from datetime import date


class UrlGenerator(object):
    @staticmethod
    def gen_search_article_url(keyword, search_type=1, page=1, time_range=0,
                               article_type='all', ft=None, et=None):
        """

        :param keyword: official account name
        :param page: page number, default is 1
        :param time_range: 0 for anytime, 1 for one day, 2 for one week, 3 for one month, 4 for one year, 5 for custom range
        :param article_type: 含有内容的类型 image 有图 / video 有视频 / rich 有图和视频 / all 啥都有 默认是 all
        :param ft: 当 time_range 是 specific 时，ft 代表开始时间，如： 2017-07-01
        :param et: 当 time_range 是 specific 时，et 代表结束时间，如： 2017-07-15
        :param search_type: 1 for searching official accounts 2 for searching articles, default is 1
        :return: url of search result

        search_type = 1
        搜索页面URL生成器 搜索给定keyword的相关公众号
        输入是公众号名 输出是拼接好的url
        模拟在搜狗微信网站上手动搜索给定公众号的过程
        EX
        输入 大纽约吃货小分队
        输出 http://weixin.sogou.com/weixin?type=1&page=1&ie=utf8&query=大纽约吃货小分队

        search_type = 2
        搜索页面URL生成器 搜索给定keyword的相关文章

        """
        assert isinstance(page, int) and page > 0
        assert time_range in [0, 1, 2, 3, 4, 5]

        if time_range == 5:
            assert isinstance(ft, date)
            assert isinstance(et, date)
            assert ft <= et
        else:
            ft = ''
            et = ''

        iteration_image = 458754
        iteration_video = 458756
        if article_type == 'rich':
            iteration = '{},{}'.format(iteration_image, iteration_video)
        elif article_type == 'image':
            iteration = iteration_image
        elif article_type == 'video':
            iteration = iteration_video
        else:
            iteration = ''

        qs_dict = dict()
        qs_dict['type'] = search_type
        qs_dict['page'] = page
        qs_dict['ie'] = 'utf8'
        qs_dict['query'] = keyword
        qs_dict['iteration'] = iteration
        if time_range != 0:
            qs_dict['tsn'] = time_range
            qs_dict['ft'] = str(ft)
            qs_dict['et'] = str(et)
        return 'http://weixin.sogou.com/weixin?{}'.format(urllib.parse.urlencode(qs_dict))

