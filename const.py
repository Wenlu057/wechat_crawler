from functools import wraps


def Const(cls):
    @wraps(cls)
    def new_setattr(self, name, value):
        raise Exception('const : {} can not be changed'.format(name))

    cls.__setattr__ = new_setattr
    return cls

@Const
class _CookieConst(object):
    IPLOC = 'US'
    SUIR = '1522853603'
    SUV = '1522853622627738'
    ABTEST = '6|1522793716|v1'
    SUID= 'B45858412013940A000000005AC540A3'
    PHPSESSID= 'hqd94hian8h9g5g5a7rek22pd7'
    SNUID= '639BC5692024483D6E28948D212316AF'
    seccodeRight= 'success'
    successCount= '1|Thu 05 Apr 2018 17:36:08 GMT'
    ld = 'lkllllllll2zeU9llllllVrpWbolllllyqPYHllllxylllllxylll5@@@@@@@@@@'

@Const
class _DirConst(object):
    BASE_DIR = './gzh_crawler_dataset/'


@Const
class _ErrorCode(object):
    SUCCESS = 0
    REQUEST_BLOCKED = 1
    SAVE_FAILURE = 2
    OTHER_ERROR = 3


@Const
class _Const(object):
    cookie_value = _CookieConst()
    dir_const = _DirConst()
    program_output_code = _ErrorCode


CrawlerConst = _Const()
