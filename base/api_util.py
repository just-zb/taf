from common.assertions import Assertions
from common.read_yaml import ReadYaml
from common.send_request import SendRequest
from conf.operConfig import OperConfig


class RequestBase:
    def __init__(self):
        self.read = ReadYaml()
        self.conf = OperConfig()
        self.run = SendRequest()
        self.asserts = Assertions()

    # TODO
    def replace_load(self, data):
        return data

    def specification_yaml(self, base_info, test_case):
        """
            1. 替换yaml文件中的参数
            2. 发送接口请求
            3. 处理接口响应信息
        :param base_info:
        :param test_case:
        :return:
        """
        try:
            params_type = ['data', 'json', 'params']

            # TODO add allure
            url_host = self.conf.get_section_data('api_env', 'host')
            url = url_host + base_info['url']
            api_name = base_info['api_name']
            method = base_info['method']
            header = self.replace_load(base_info['header'])
            cookies = None
            if base_info.get('cookies') is not None:
                cookies = eval(self.replace_load(base_info['cookies']))

            # test_case 是一个字典，包含了名称,数据,验证方法等信息
            case_name = test_case.pop('case_name')
            # 替换yaml文件中的参数，可能包含请求参数、验证方法、提取数据等参数
            # test_case['validation'] = self.replace_load(test_case.get('validation'))
            # validation = eval(test_case.pop('validation'))
            test_case.pop('validation')

            extract = test_case.pop('extract', None)
            extract_list = test_case.pop('extract_list', None)

            # replace_load 接口请求参数
            for k, v in test_case.items():
                if k in params_type:
                    test_case[k] = self.replace_load(v)

            # TODO 文件上传

            # 发送接口请求
            res = self.run.run(name=api_name,
                               url=url,
                               case_name=case_name,
                               header=header,
                               method=method,
                               cookies=cookies,
                               **test_case
                               )

            # TODO 处理接口响应信息

        except Exception as e:
            raise e

    def extract_data(self, test_case_extract, response):
        pass

    def extract_data_list(self, testcase_extract_list, response):
        pass
