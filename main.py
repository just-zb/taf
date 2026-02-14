import os

import pytest

if __name__ == '__main__':
    pytest.main(
        [
            '-s',
            '-v',
            '--alluredir=./report/temp',
            './testcase',
            '--clean-alluredir'
        ]
    )
    os.system('allure serve ./report/temp')