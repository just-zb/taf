import time

from common.read_yaml import ReadYaml


class DebugTalk:
    """
    debug_talk.py文件主要用于存放接口测试过程中需要用到的函数，例如：数据加密、时间戳等函数，供yaml文件调用
    """

    @staticmethod
    def get_extract_data(node_name):
        data = ReadYaml.read_extract_yaml(node_name)
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
