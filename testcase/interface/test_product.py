from pathlib import Path

import pytest

from base.api_util import RequestBase
from common.read_yaml import get_test_case_yaml

TESTCASE_DIR = Path(__file__).parent

class TestLogin:
    @pytest.mark.parametrize("base_info,test_case", get_test_case_yaml(TESTCASE_DIR / "login.yaml"))
    def test_login(self,base_info,test_case):
        RequestBase().specification_yaml(base_info,test_case)