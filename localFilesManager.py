import os
from const import CrawlerConst
import requests
from imageProcessingHandler import ImageProcessingHandler


class LocalFilesManager(object):

    def __init__(self, gzh_name, date, article_title):
        self.gzh_name = gzh_name
        self.date = date
        self.title = article_title

    def create_gzh_dir(self):
        gzh_dir = os.path.join(CrawlerConst.dir_const.BASE_DIR, self.gzh_name)
        if not os.path.isdir(gzh_dir):
            os.makedirs(gzh_dir, exist_ok=True)  # 如果不存在，创建公众号的dir

    def create_article_dir(self):
        path_to_article = self.__get_path_to_article()
        os.makedirs(path_to_article, exist_ok=True)

    def save_pics_to_local(self, url, img_file):
        """

        :param url: 指定从哪个url下载图片
        :param img_file: 指定图片名称来组合本地路径
        :return: 返回是否下载成功
        """
        r = requests.get(url, stream=True)
        img_path = os.path.join(self.__get_path_to_article(), img_file)
        if not os.path.exists(img_path):
            try:
                with open(img_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=128):
                        f.write(chunk)
            except IOError:
                return CrawlerConst.program_output_code.SAVE_FAILURE
            ImageProcessingHandler.convert_to_gray(img_path)
        return CrawlerConst.program_output_code.SUCCESS

    def save_html_to_local(self, html):
        """

        :param html: 指定想要存储的html
        :return: 返回是否成功存储
        """
        html_file = self.title + '.html'
        html_path = os.path.join(self.__get_path_to_article(), html_file)
        if not os.path.exists(html_path):
            try:
                with open(html_path, 'w') as text_file:
                    text_file.write(html)
            except IOError:
                return CrawlerConst.program_output_code.SAVE_FAILURE
            print('Saved html file to %s' % html_path)
        return CrawlerConst.program_output_code.SUCCESS

    def __get_path_to_article(self):
        gzh_dir = os.path.join(CrawlerConst.dir_const.BASE_DIR, self.gzh_name)
        path_to_article = os.path.join(os.path.join(gzh_dir, self.date), self.title)
        return path_to_article
