#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# WeAuth is released under the GNU GENERAL PUBLIC LICENSE v3 (GPLv3.0) license.
# datetime： 2025/1/7 22:55 
# ide： PyCharm
# file: mcsm.py.py
import requests

class MCSM:
    def __init__(self):
        super().__init__()
        ...

    @staticmethod
    def test_connection(mcsm_adr, mcsm_api, uuid, remote_uuid) -> int:
        """
        测试与MCSM的连接
        :param mcsm_adr:
        :param mcsm_api:
        :param uuid:
        :param remote_uuid:
        :return: http请求状态码或-1
        """
        param = {
            'uuid': uuid,
            'remote_uuid': remote_uuid,
            'apikey': mcsm_api,
            'command': '1'
        }
        try:
            response = requests.get(url=mcsm_adr, params=param)
            # print(response.status_code)
        except:
            return -1
        else:
            return response.status_code

    @staticmethod
    def push_command(adr, api, uuid, remote_uuid, command) -> int:
        """

        :param adr:
        :param api:
        :param uuid:
        :param remote_uuid:
        :param command:
        :return: http请求状态码或-1
        """
        addr = adr + 'api/protected_instance/command'
        param = {
            'uuid': uuid,
            'remote_uuid': remote_uuid,
            'apikey': api,
            'command': command
        }
        try:
            response = requests.get(url=addr, params=param)
            # print(response.status_code)
            return response.status_code
        except ConnectionError:
            return -1
        else:
            return response.status_code
