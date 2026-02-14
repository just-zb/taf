import os

import pytest

if __name__ == '__main__':
    # 运行测试用例，生成allure报告数据
    pytest.main(
        [
            '-s',# 显示测试用例执行过程中的输出信息
            '-v',# 显示测试用例的详细信息
            '--alluredir=./report/temp', # 指定生成allure报告数据的目录
            './testcase', # 指定测试用例所在的目录
            '--clean-alluredir' # 在生成allure报告数据之前清空指定目录中的旧数据
        ]
    )
    # os.system('allure serve ./report/temp')