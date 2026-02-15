from pathlib import Path

import pytest

from base.api_util import RequestBase
from common.read_yaml import ReadYaml

TESTCASE_DIR = Path(__file__).parent

class TestLogin:
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("base_info,test_case", ReadYaml.read_test_case_yaml(TESTCASE_DIR / "login.yaml"))
    def test_login(self,base_info,test_case):
        RequestBase().specification_yaml(base_info,test_case)

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("base_info,test_case", ReadYaml.read_test_case_yaml(TESTCASE_DIR / "addUser.yaml"))
    def test_add_user(self, base_info, test_case):
        # allure.dynamic.title(test_case['case_name'])
        RequestBase().specification_yaml(base_info, test_case)