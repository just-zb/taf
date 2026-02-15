import json
import re
from json import JSONDecodeError

import allure
import jsonpath

from common.assertions import Assertions
from common.debug_talk import DebugTalk
from common.read_yaml import ReadYaml
from common.recordlog import logs
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

            api_name = base_info['api_name']
            url_host = self.conf.get_section_data('api_env', 'host')
            url = url_host + base_info['url']
            method = base_info['method']
            header = self.replace_load(base_info['header'])
            # allure attach
            allure.attach(api_name, f'接口地址：{url}', allure.attachment_type.TEXT)
            allure.attach(api_name, f'接口名称：{api_name}', allure.attachment_type.TEXT)
            allure.attach(api_name, f'请求方法：{method}', allure.attachment_type.TEXT)
            allure.attach(api_name, f'请求头：{header}', allure.attachment_type.TEXT)
            # handle cookies
            cookies = None
            if base_info.get('cookies') is not None:
                cookies = eval(self.replace_load(base_info['cookies']))

            # test_case 是一个字典，包含了名称,数据,验证方法等信息
            case_name = test_case.pop('case_name')
            allure.attach(api_name, f'测试用例名称：{case_name}', allure.attachment_type.TEXT)
            # validation 替换
            test_case['validation'] = self.replace_load(test_case.get('validation'))
            validation = eval(test_case.pop('validation'))

            # 从接口响应中提取参数
            extract = test_case.pop('extract', None)
            extract_list = test_case.pop('extract_list', None)

            # replace_load 接口请求参数
            for k, v in test_case.items():
                if k in params_type:
                    test_case[k] = self.replace_load(v)

            # 发送接口请求
            res = self.run.run(name=api_name,
                               url=url,
                               case_name=case_name,
                               header=header,
                               method=method,
                               cookies=cookies,
                               **test_case
                               )

            # 处理接口响应信息
            allure.attach(json.dumps(res.json(), ensure_ascii=False, indent=2), '接口响应信息', allure.attachment_type.JSON)
            try:
                res_json = json.loads(res.text)
                if extract is not None:
                    self.extract_data(extract, res.text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res.text)
                # 处理断言
                self.asserts.assert_result(validation, res_json, res.status_code)
            except JSONDecodeError as je:
                logs.error('系统异常或接口未请求！')
                raise je
            except Exception as e:
                logs.error(e)
                raise e

        except Exception as e:
            raise e

    def extract_data(self, test_case_extract, response):
        """
        提取接口的响应参数,支持正则表达式和json提取, 提取的数据会写入extract.yaml文件中，供后续接口调用
        :param test_case_extract: testcase文件yaml中的extract值
        :param response: 接口的实际返回值
        :return:
        """
        try:
            pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
            for key, value in test_case_extract.items():

                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                        else:
                            extract_data = {key: ext_lst.group(1)}
                        self.read.write_extract_yaml(extract_data)
                # 处理json提取器
                if '$' in value:
                    # $.data.user_token能够被jsonpath识别, 提取接口返回值中的user_token
                    ext_json = jsonpath.jsonpath(json.loads(response),value)[0]
                    if ext_json:
                        extract_data = {key: ext_json}
                        logs.info('提取接口的返回值：%s' % extract_data)
                    else:
                        extract_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                        logs.error('未提取到数据，请检查接口返回值是否为空！')
                    # 将提取到的数据写入extract.yaml文件中
                    self.read.write_extract_yaml(extract_data)
        except Exception as e:
            logs.error(str(e))
            raise e
    def extract_data_list(self, testcase_extract_list, response):
        pass
