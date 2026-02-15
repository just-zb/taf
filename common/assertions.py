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
                    # TODO add allure
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
                        # TODO add allure
                        logs.error("响应文本断言失败：预期结果为【%s】,实际结果为【%s】" % (a_value, resp_list))
        return flag

    @staticmethod
    def equals_assert(value, response):
        return 0

    @staticmethod
    def not_equals_assert(value, response):
        return 0

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
