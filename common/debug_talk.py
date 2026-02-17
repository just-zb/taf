import random
import re
import time

from common.read_yaml import ReadYaml


class DebugTalk:
    """
    debug_talk.py文件主要用于存放接口测试过程中需要用到的函数，例如：数据加密、时间戳等函数，供yaml文件调用
    """

    def __init__(self):
        self.read = ReadYaml()

    def get_extract_data(self, node_name, randoms=None):
        """
        获取extract.yaml数据，首先判断randoms是否为数字类型，如果不是就获取下一个node节点的数据
        :param node_name: extract.yaml文件中的key值
        :param randoms: randoms: int类型，0：随机读取；-1：读取全部，返回字符串形式；-2：读取全部，返回列表形式；
        其他根据列表索引取值，取第一个值为1，第二个为2，以此类推;
        :return:
        """
        data = self.read.read_extract_yaml(node_name)
        if randoms is not None and bool(re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$').match(randoms)):
            randoms = int(randoms)
            if randoms == 0:
                data = random.choice(data)
            elif randoms == -1:
                data = ','.join(data)
            elif randoms == -2:
                data = ','.join(data).split(',')
            else:
                data = data[randoms - 1]
        else:
            data = self.read.read_extract_yaml(node_name, randoms)
        return data

    @staticmethod
    def timestamp():
        """获取当前时间戳，10位"""
        t = int(time.time())
        return t

    @staticmethod
    def get_baseurl(host):
        from conf.oper_config import OperConfig
        conf = OperConfig()
        base_url = conf.get_section_data('api_env', host)
        return base_url
