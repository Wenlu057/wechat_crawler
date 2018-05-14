from lxml import etree
import re
import json
from bs4 import BeautifulSoup
from localFilesManager import LocalFilesManager


class HtmlParser(object):

    @staticmethod
    def parse_gzh_list_html(response):
        """
        获取公众号历史消息页面的url
        :param response: 输入是发送请求得到的公众号列表response
        :return: 输出是公众号历史页面的url和拿到的第一个公众的名字
        """
        page = etree.HTML(response.text)
        first_gzh = page.xpath('//ul[@class="news-list2"]/li[1]')[0]  # get first gzh
        url = first_gzh.xpath('div/div[1]/a/@href')[0]  # get the url of first gzh
        first_gzh_name = first_gzh.xpath('div/div[2]/p[1]/a')[0].xpath('string(.)')
        return url, first_gzh_name

    @staticmethod
    def parse_history_article_list_html(response, days=3):
        """

        :param response:  输入是发送请求得到的某个指定公众号的历史文章页面response :param days: 指定你需要获取几天的历史文章
        :return: 一个列表含有多个历史文章的相应信息，
        相应信息包括 [send_id, datetime, type, main, title, abstract, fileid, content_url, source_url, cover, author,
        copyright_stat]
        """
        article_ls = re.compile('var msgList = (.*?)}}]};').findall(response.text)  # 用正则表达抓取历史文章的部分
        article_str = article_ls[0] + '}}]}'  # 已经拿到了msgList的内容
        article_json = json.loads(article_str)  # 将json转变成python对象
        items = list()
        for element in article_json['list'][:days]:  # 遍历十个历史文章列表
            if str(element['comm_msg_info'].get('type', '')) != '49':
                continue
            comm_msg_info = element['comm_msg_info']  # dict
            app_msg_ext_info = element['app_msg_ext_info']  # dict
            send_id = comm_msg_info.get('id', '')
            msg_datetime = comm_msg_info.get('datetime', '')
            msg_type = str(comm_msg_info.get('type', ''))
            is_multi = app_msg_ext_info.get('is_multi', '')
            items.append({
                'send_id': send_id,
                'datetime': msg_datetime,
                'type': msg_type,
                'main': 1,
                'title': app_msg_ext_info.get('title', ''),
                'abstract': app_msg_ext_info.get('digest', ''),
                'fileid': app_msg_ext_info.get('fileid', ''),
                'content_url': HtmlParser.__auto_complete_url(app_msg_ext_info.get('content_url')),  # 自动补全url并替换转义
                'source_url': app_msg_ext_info.get('source_url', ''),
                'cover': app_msg_ext_info.get('cover', ''),
                'author': app_msg_ext_info.get('author', ''),
                'copyright_stat': app_msg_ext_info.get('copyright_stat', '')
            })
            if is_multi == 1:  # 当天有多篇文章
                multi_app_msg_item_list = app_msg_ext_info.get('multi_app_msg_item_list', '')  # 列表格式
                for multi_app_msg_item in multi_app_msg_item_list:
                    items.append({
                        'send_id': send_id,
                        'datetime': msg_datetime,
                        'type': msg_type,
                        'main': 1,
                        'title': multi_app_msg_item.get('title', ''),
                        'abstract': multi_app_msg_item.get('digest', ''),
                        'fileid': multi_app_msg_item.get('fileid', ''),
                        'content_url': HtmlParser.__auto_complete_url(multi_app_msg_item.get('content_url')),
                        # 自动补全url并替换转义
                        'source_url': multi_app_msg_item.get('source_url', ''),
                        'cover': multi_app_msg_item.get('cover', ''),
                        'author': multi_app_msg_item.get('author', ''),
                        'copyright_stat': multi_app_msg_item.get('copyright_stat', '')
                    })
        return list(filter(lambda x: x['content_url'], items))

    @staticmethod
    def parse_history_article_html(response, gzh_name):
        """

        :param response: 发送请求得到的某个历史文章页面的response
        :param gzh_name: 指定是哪个公众号以便设计本地存储路径
        :return: 返回是否成功parse并下载图片和html至本地
        """
        removeJS = re.sub(r"(?s)<script.*?</script>", r"", response.text)  # 删除所有js
        replaceDatasrc = re.sub(r"data-src", r"src", removeJS)  # replace所有data-src
        soup = BeautifulSoup(replaceDatasrc, features='lxml')  # 创建beautifulsoup树
        for img in soup.find_all('img', {"data-type": "gif"}):  # 删除所有gif
            img.decompose()
        date = soup.find('em', {"id": "post-date"}).get_text()
        title = soup.title.get_text().replace('/', '-')
        local_files_manager = LocalFilesManager(gzh_name, date, title)
        local_files_manager.create_article_dir()
        # 找到所有image的url， 下载图片并且替换所有url为本地path
        img_links = soup.find_all("img", {"src": re.compile('.*?640\?wx_fmt=[jpeg|png]')})
        for link in img_links:
            img_name = re.findall(r"(mmbiz|mmbiz_jpg|mmbiz_png)/(.*?)/", link['src'])[0][1]
            img_file = img_name + '.jpeg' if link['data-type'] == 'jpeg' else img_name + '.png'
            save_res = local_files_manager.save_pics_to_local(link['src'], img_file)
            link['src'] = img_file
        # 存储html
        save_res = local_files_manager.save_html_to_local(soup.prettify())
        return save_res

    @staticmethod
    def __auto_complete_url(url):
        url = url.replace('&amp;', '&')
        return ('http://mp.weixin.qq.com{}'.format(url)
                if 'http://mp.weixin.qq.com' not in url else url) if url else ''
