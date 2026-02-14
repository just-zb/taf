import json

from common.recordlog import logs
from conf import setting


class SendRequest:
    def __init__(self, cookies=None):
        self.cookies = cookies

    def get(self,url,header,data):
        pass

    def post(self,url,header,data):
        pass

    def request(self, **kwargs):
        pass

    def run(self,name, url, case_name, header, method, cookies=None, **kwargs):
        """
        接口请求
        :param name: 接口名
        :param url: 接口地址
        :param case_name: 测试用例
        :param header:请求头
        :param method:请求方法
        :param cookies：默认为空
        :param kwargs: 请求参数，根据yaml文件的参数类型
        :return:
        """
        try:
            logs.info('接口名称：%s' % name)
            logs.info('请求地址：%s' % url)
            logs.info('请求方式：%s' % method)
            logs.info('测试用例名称：%s' % case_name)
            logs.info('请求头：%s' % header)
            logs.info('Cookie：%s' % cookies)
            req_params = json.dumps(kwargs, ensure_ascii=False)

            if 'data' in kwargs.keys():
                logs.info("请求参数：%s" % kwargs)
            elif 'json' in kwargs.keys():
                logs.info("请求参数：%s" % kwargs)
            elif 'params' in kwargs.keys():
                logs.info("请求参数：%s" % kwargs)
        except Exception as e:
            logs.error(e)

        response = self.request(method=method,
                                url=url,
                                headers=header,
                                cookies=cookies,
                                timeout=setting.API_TIMEOUT,
                                verify=False,
                                **kwargs)
        return response
