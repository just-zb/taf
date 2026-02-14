class RequestBase:
    def __init__(self):
        pass

    def specification_yaml(self,base_info, test_case):
        try:
            params_type = ['data', 'json', 'params']

        except Exception as e:
            raise e