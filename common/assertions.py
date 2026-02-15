from common.recordlog import logs


class Assertions:
    """
    接口断言
    """
    def contains_assert(self,value, response, status_code):
        # TODO
        return 0
    def equals_assert(self,value, response):
        return 0
    def not_equals_assert(self,value, response):
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