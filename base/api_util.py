import json

from common.assertions import Assertions
from common.debug_talk import DebugTalk
from common.read_yaml import ReadYaml
from common.send_request import SendRequest
from conf.oper_config import OperConfig


class RequestBase:
    def __init__(self):
        self.read = ReadYaml()
        self.conf = OperConfig()
        self.run = SendRequest()
        self.asserts = Assertions()

    @classmethod
    def replace_load(cls, data):
        """
        查找yaml文件中的${}，解析函数并替换数据
        :param data: 解析后的数据，可能是字符串，也可能是字典
        :return: 替换后的数据
        """
        str_data = data
        if not isinstance(data, str):
            # 把json转为字符串
            str_data = json.dumps(data, ensure_ascii=False)
        for i in range(str_data.count('${')):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]

                # get function name in ${}
                func_name = ref_all_params[2:ref_all_params.index("(")]
                # get function params in ${}
                func_params = ref_all_params[ref_all_params.index("(") + 1:ref_all_params.index(")")]

                extract_data = getattr(DebugTalk(), func_name)(*func_params.split(',') if func_params else "")
                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)

                str_data = str_data.replace(ref_all_params, str(extract_data))
                print('通过解析后替换的数据：', str_data)

        # 还原数据
        if data and isinstance(data, dict):
            # 如果是header,data格式为字典
            data = json.loads(str_data)
        else:
            # 如果是字符串
            data = str_data
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
            # TODO add validation
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
