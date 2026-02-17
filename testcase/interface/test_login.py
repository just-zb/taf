from pathlib import Path

import allure
import pytest

from base.api_util import RequestBase
from base.generateId import m_id, c_id
from common.read_yaml import ReadYaml

TESTCASE_DIR = Path(__file__).parent
@allure.feature(next(m_id)+ "测试登录模块")
class TestLogin:

    @allure.story(next(c_id)+"查询用户")
    @pytest.mark.parametrize("base_info,test_case", ReadYaml.read_test_case_yaml(TESTCASE_DIR / "queryUser.yaml"))
    def test_query_user(self,base_info, test_case):
        allure.dynamic.title(test_case['case_name'])
        RequestBase().specification_yaml(base_info, test_case)