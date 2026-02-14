import pytest
from pathlib import Path
from common.read_yaml import get_test_case_yaml

TESTCASE_DIR = Path(__file__).parent

class TestUserApi:

    @pytest.mark.parametrize("base_info, test_case",get_test_case_yaml(TESTCASE_DIR / "addUser.yaml"))
    def test_add_user(self,base_info,test_case):
        pass

