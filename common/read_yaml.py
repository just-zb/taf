import os

import yaml

from common.recordlog import logs
from conf.setting import FILE_PATH

class ReadYaml:
    @staticmethod
    def read_test_case_yaml(file_path):
        """
            读取yaml文件中的测试用例数据
        :param file_path: yaml文件路径
        :return: 包含测试用例数据的列表，每个元素是一个包含base_info和test_case的列表
        """
        test_case_list = []
        try:
            with open(file_path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if len(data) <= 1:
                    yaml_data = data[0]
                    base_info = yaml_data.get('baseInfo')
                    for ts in yaml_data.get('testCase'):
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

    @classmethod
    def read_extract_yaml(cls, node_name, second_node_name=None):

        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            logs.error('extract.yaml不存在')
            with open(FILE_PATH['EXTRACT'], 'w', encoding='utf-8') as f:
                f.close()
            logs.info('extract.yaml创建成功！')

        # 读取extract.yaml文件中的数据
        try:
            with open(FILE_PATH['EXTRACT'], encoding='utf-8') as f:
                ext_data = yaml.safe_load(f)
                if second_node_name is None:
                    return ext_data[node_name]
                else:
                    return ext_data[node_name][second_node_name]
        except Exception as e:
            logs.error(f"[extract.yaml]没有找到：{node_name},--%s" % e)



