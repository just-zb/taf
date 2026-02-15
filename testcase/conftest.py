"""
-function：每一个函数或方法都会调用
-class：每一个类调用一次，一个类中可以有多个方法
-module：每一个.py文件调用一次，该文件内又有多个function和class
-session：是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module,整个会话只会运行一次
-autouse：默认为false，不会自动执行，需要手动调用，为true可以自动执行，不需要调用
- yield：前置、后置
"""
from pathlib import Path

import allure
import pytest

from base.api_util import RequestBase
from common.read_yaml import ReadYaml
from common.recordlog import logs

PRJ_DIR = Path(__file__).parent.parent


@pytest.fixture(scope='function', autouse=True)
def start_test_and_end():
    print('-------------接口测试开始--------------')
    yield
    print('-------------接口测试结束--------------')

@allure.story("登录")
@pytest.fixture(scope='session', autouse=True)
def system_login():
    try:
        api_info = ReadYaml.read_test_case_yaml(PRJ_DIR / "data/loginName.yaml")
        RequestBase().specification_yaml(api_info[0][0], api_info[0][1])
    except Exception as e:
        logs.error(f'登录接口出现异常，导致后续接口无法继续运行，请检查程序！，{e}')
        exit()
