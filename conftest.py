import pytest

from common.read_yaml import ReadYaml

@pytest.fixture(scope="session", autouse=True)
def clear_extract_yaml():
    ReadYaml.clear_extract_yaml()

    # TODO 删除旧报告