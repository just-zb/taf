import allure
import pytest
from pathlib import Path

from base.api_util_business import RequestBaseBusiness
from base.generateId import m_id, c_id
from common.read_yaml import ReadYaml

BASE_DIR = Path(__file__).resolve().parent

@allure.feature(next(m_id) + '电子商务管理系统（业务场景）')
class TestBusinessInterface:
    @allure.story(next(c_id) + '商品列表到下单支付流程')
    @pytest.mark.parametrize("case_info", ReadYaml.read_test_case_yaml(BASE_DIR / "businessCase.yaml"))
    def test_business_interface(self, case_info):
        allure.dynamic.title(case_info['baseInfo']["api_name"])
        RequestBaseBusiness().specification_yaml(case_info)
