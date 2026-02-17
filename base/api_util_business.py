import json
import re
import traceback
from json import JSONDecodeError

import allure
import jsonpath

from base.api_util import RequestBase
from common.assertions import Assertions
from common.debug_talk import DebugTalk
from common.read_yaml import ReadYaml
from common.recordlog import logs
from common.send_request import SendRequest
from conf.oper_config import OperConfig



class RequestBaseBusiness:
    def __init__(self):
        self.read = ReadYaml()
        self.conf = OperConfig()
        self.run = SendRequest()
        self.asserts = Assertions()
        self.requestBase = RequestBase()

    @staticmethod
    def handle_yaml_list(data_dict):
        try:
            for k,v in data_dict.items():
                if isinstance(v, list):
                    # TODO
                    data_dict[k] = [str(a) for a in v]
            return data_dict
        except Exception as e:
            logs.error(str(traceback.format_exc()))

    def specification_yaml(self, case_info):
        try:
            params_type = ['data', 'json', 'params']

            api_name = case_info['baseInfo']['api_name']
            url_host = self.conf.get_section_data('api_env', 'host')
            url = url_host + case_info['baseInfo']['url']
            method = case_info['baseInfo']['method']
            header = self.requestBase.replace_load(case_info['baseInfo']['header'])
            # allure attach
            allure.attach(api_name, f'接口地址：{url}', allure.attachment_type.TEXT)
            allure.attach(api_name, f'接口名称：{api_name}', allure.attachment_type.TEXT)
            allure.attach(api_name, f'请求方法：{method}', allure.attachment_type.TEXT)
            allure.attach(api_name, f'请求头：{header}', allure.attachment_type.TEXT)
            # handle cookies
            cookies = None
            try:
                cookies = self.requestBase.replace_load(case_info['baseInfo']['cookies'])
            except Exception as e:
                logs.error('没有cookie参数，继续执行接口请求！')

            for tc in case_info['testCase']:
                case_name = tc.pop('case_name')
                allure.attach(api_name, f'测试用例名称：{case_name}', allure.attachment_type.TEXT)
                # validation 替换
                tc['validation'] = self.requestBase.replace_load(tc.get('validation'))
                validation = eval(tc.pop('validation'))

                # 从接口响应中提取参数
                extract = tc.pop('extract', None)
                extract_list = tc.pop('extract_list', None)

                # replace_load 接口请求参数
                for k, v in tc.items():
                    if k in params_type:
                        tc[k] = self.requestBase.replace_load(v)

                # 发送接口请求
                res = self.run.run(name=api_name,
                                   url=url,
                                   case_name=case_name,
                                   header=header,
                                   method=method,
                                   cookies=cookies,
                                   **tc
                                   )

                # 处理接口响应信息
                allure.attach(json.dumps(res.json(), ensure_ascii=False, indent=2), '接口响应信息', allure.attachment_type.JSON)

                try:
                    res_json = json.loads(res.text)
                    if extract is not None:
                        self.requestBase.extract_data(extract, res.text)
                    if extract_list is not None:
                        self.requestBase.extract_data_list(extract_list, res.text)
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
