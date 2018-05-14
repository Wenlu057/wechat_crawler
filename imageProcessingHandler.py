from scipy import misc
import numpy as np


class ImageProcessingHandler(object):
    @staticmethod
    def convert_to_gray(image_path):
        """

        :param image_path: 指定图片路径
        将图片灰化后替换原油彩色图片
        """
        image_data = misc.imread(image_path)
        if len(image_data.shape) > 2:
            grey = np.mean(image_data, -1)
            misc.imsave(image_path, grey)