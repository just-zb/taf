from common.recordlog import logs
from conf import setting
import configparser
import traceback

class OperConfig:
    def __init__(self, filepath=None):
        if filepath is None:
            self.__filepath = setting.FILE_PATH['CONFIG']
        else:
            self.__filepath = filepath

        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__filepath, encoding='utf-8')
        except Exception as e:
            logs.error(e)

    def get_section_data(self, section, option):
        """
        根据section和option获取ini文件中的值
        :param section: ini文件头部
        :param option: 头部值
        :return:
        """
        try:
            value = self.conf.get(section, option)
            return value
        except Exception as e:
            logs.error(str(traceback.format_exc()))
            return ''

