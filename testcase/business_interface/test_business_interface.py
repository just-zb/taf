import allure
import pytest
from pathlib import Path

from base.api_util_business import RequestBaseBusiness
from common.read_yaml import ReadYaml

BASE_DIR = Path(__file__).resolve().parent


class TestBusinessInterface:
    @allure.story('商品列表到下单支付流程')
    @pytest.mark.parametrize("case_info", ReadYaml.read_test_case_yaml(BASE_DIR / "businessCase.yaml"))
    def test_business_interface(self, case_info):
        allure.dynamic.title(case_info['baseInfo']["api_name"])
        RequestBaseBusiness().specification_yaml(case_info)
