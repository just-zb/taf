from pathlib import Path

import pytest

from base.api_util import RequestBase
from common.read_yaml import ReadYaml

TESTCASE_DIR = Path(__file__).parent

class TestLogin:

    @pytest.mark.parametrize("base_info,test_case", ReadYaml.read_test_case_yaml(TESTCASE_DIR / "queryUser.yaml"))
    def test_query_user(self,base_info, test_case):
        RequestBase().specification_yaml(base_info, test_case)