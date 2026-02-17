import operator

import allure
import jsonpath

from common.recordlog import logs


class Assertions:
    """
    接口断言
    """

    @staticmethod
    def contains_assert(value, response, status_code):
        flag = 0
        for a_key, a_value in value.items():
            if a_key == "status_code":
                if a_value != status_code:
                    flag += 1
                    allure.attach(f"预期结果：{a_value}\n实际结果：{status_code}", '响应代码断言结果:失败',attachment_type=allure.attachment_type.TEXT)
                    logs.error("contains断言失败：接口返回码【%s】不等于【%s】" % (status_code, a_value))
            else:
                resp_list = jsonpath.jsonpath(response, "$..%s" % a_key)
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    a_value = None if a_value.upper() == "NONE" else a_value
                    if a_value in resp_list:
                        logs.info("字符串包含断言成功：预期结果【%s】,实际结果【%s】" % (a_value, resp_list))
                    else:
                        flag += 1
                        allure.attach(f"预期结果：{a_value}\n实际结果：{resp_list}", '响应文本断言结果：失败',
                                      attachment_type=allure.attachment_type.TEXT)
                        logs.error("响应文本断言失败：预期结果为【%s】,实际结果为【%s】" % (a_value, resp_list))
        return flag

    @staticmethod
    def equals_assert(expected_results, actual_results):
        flag =0
        if isinstance(expected_results, dict) and isinstance(actual_results, dict):
            # 找出实际结果与预期结果共同的key
            common_keys = list(expected_results.keys() & actual_results.keys())[0]
            # 根据相同的key去实际结果中获取，并重新生成一个实际结果的字典
            new_actual_results = {common_keys: actual_results[common_keys]}
            eq_assert = operator.eq(new_actual_results, expected_results)
            if eq_assert:
                logs.info(f"相等断言成功：接口实际结果：{new_actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            else:
                flag += 1
                logs.error(f"相等断言失败：接口实际结果{new_actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        else:
            raise TypeError('相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag

    @staticmethod
    def not_equals_assert(actual_results, expected_results):
        flag = 0
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            # 找出实际结果与预期结果共同的key
            common_keys = list(expected_results.keys() & actual_results.keys())[0]
            # 根据相同的key去实际结果中获取，并重新生成一个实际结果的字典
            new_actual_results = {common_keys: actual_results[common_keys]}
            eq_assert = operator.ne(new_actual_results, expected_results)
            if eq_assert:
                logs.info(f"不相等断言成功：接口实际结果：{new_actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '不相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            else:
                flag += 1
                logs.error(f"不相等断言失败：接口实际结果{new_actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '不相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        else:
            raise TypeError('不相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag

    def assert_result(self, expected, response, status_code):
        try:
            logs.info("yaml文件预期结果：%s" % expected)
            total_flag = 0
            for yq in expected:
                for key, value in yq.items():
                    if key == "contains":
                        total_flag += self.contains_assert(value, response, status_code)
                    elif key == "eq":
                        total_flag += self.equals_assert(value, response)
                    elif key == "ne":
                        total_flag += self.not_equals_assert(value, response)
                    else:
                        logs.error("不支持此种断言方式")


        except Exception as e:
            logs.error('接口断言异常，请检查yaml预期结果值是否正确填写!')
            raise e
        if not total_flag:
            logs.info("接口断言成功")
            assert True
        else:
            logs.error("接口断言失败")
            assert False
