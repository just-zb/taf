import yaml

from common.recordlog import logs


def get_test_case_yaml(file_path):
    """
        读取yaml文件中的测试用例数据
    :param file_path: yaml文件路径
    :return: 包含测试用例数据的列表，每个元素是一个包含base_info和test_case的列表
    """
    test_case_list = []
    try:
        with open(file_path,'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if len(data) == 0:
                return None
            if len(data) == 1:
                yam_data = data[0]
                base_info = yam_data.get('baseInfo')
                for ts in yam_data.get('testCase'):
                    param = [base_info, ts]
                    test_case_list.append(param)
                return test_case_list
            else:
                return data

    except UnicodeDecodeError:
        logs.error(f"[{file_path}] 文件编码格式错误")
    except FileNotFoundError:
        logs.error(f'[{file_path}]文件未找到，请检查路径是否正确')
    except Exception as e:
        logs.error(f"[{file_path}] 未知错误, {str(e)}")
