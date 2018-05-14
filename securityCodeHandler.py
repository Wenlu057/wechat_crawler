import tempfile
from PIL import Image
import time


class SecurityCodeHandler(object):
    def __init__(self, url, resp, session, ws_cache):
        self.url = url
        self.resp = resp
        self.session = session
        self.ws_cache = ws_cache

    def handle_sogou_security_code(self):
        millis = int(round(time.time() * 1000))
        r_captcha = self.session.get('http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(millis))
        if not r_captcha.ok:
            print('Antispider page not found error!', r_captcha)
        r_unlock = self.__unlock_sogou_callback_example(r_captcha.content)
        if r_unlock['code'] != 0:
            print(
                '[WechatSogouAPI identify image] code: {code}, msg: {msg}'.format(code=r_unlock.get('code'),
                                                                                  msg=r_unlock.get('msg')))
        else:
            self.__set_cache(self.session.cookies.get('SUID'), r_unlock['id'])

    @staticmethod
    def __identify_image_callback_manually(img):
        """
        :param img: the image showing the security codes
        :return: trigger an input in console for user to type the security codes in the image

        得到当前验证码图片，显示出来并让用户输入图片中的验证码
        """
        with tempfile.TemporaryFile() as fp:
            fp.write(img)
            fp.seek(0)
            im = Image.open(fp)
            im.show()
        return input("please input code: ")

    def __set_cache(self, suv, snuid):
        self.ws_cache.set('suv', suv)
        self.ws_cache.set('snuid', snuid)

    def __unlock_sogou_callback_example(self, img):
        # no use resp
        url_quote = self.url.split('weixin.sogou.com/')[-1]

        unlock_url = 'http://weixin.sogou.com/antispider/thank.php'
        data = {
            'c': self.__identify_image_callback_manually(img),
            'r': '%2F' + url_quote,
            'v': 5
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + url_quote
        }
        r_unlock = self.session.post(unlock_url, data, headers=headers)
        if not r_unlock.ok:
            print(
                'unlock[{}] failed: {}'.format(unlock_url, r_unlock.text, r_unlock.status_code))
        return r_unlock.json()