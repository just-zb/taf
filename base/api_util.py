from common.send_request import SendRequest
from conf.operConfig import OperConfig


class RequestBase:
    def __init__(self):
        self.conf = OperConfig()
        self.run = SendRequest()

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
            api_name = base_info['api_name']
            url = url_host + base_info['url']
            method = base_info['method']
            header = self.replace_load(base_info['header'])
            cookie = None
            if base_info.get('cookies') is not None:
                cookie = eval(self.replace_load(base_info['cookies']))
            case_name = test_case.pop('case_name')
            val = self.replace_load(test_case.get('validation'))
            test_case['validation'] = val
            validation = eval(test_case.pop('validation'))

            extract = test_case.pop('extract', None)
            extract_list = test_case.pop('extract_list', None)

            # 接口请求参数
            for k, v in test_case.items():
                if k in params_type:
                    test_case[k] = self.replace_load(v)

            # TODO 文件上传

            res = self.run.run(name=api_name,
                               url=url,
                               case_name=case_name,
                               header=header,
                               method=method,
                               cookie=cookie,
                               **test_case
                               )

            # TODO 处理接口响应信息

        except Exception as e:
            raise e

    def extract_data(self, test_case_extract, response):
        pass

    def extract_data_list(self, testcase_extract_list, response):
        pass
