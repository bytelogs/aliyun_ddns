#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2019/4/8 14:04
# @Author    :balich
# @File      :aliddns.py

"""
python3环境

https://ifconfig.co/json
https://wtfismyip.com/text
https://api.aliyun.com/
"""
import datetime
import json
import sys
import requests
import logging
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest


def get_public_ip():
    """
    get public ip address
    return ip_value
    """
    try:
        get_ip_req = requests.get('https://ifconfig.co/json', timeout=30).content.decode()
    except Exception as e_message:
        return 'An error occurred! Error MSG: ' + str(e_message)
    else:
        current_ip = json.loads(get_ip_req)['ip']
        return current_ip


def get_domain_record(client, domain, sub_domain):
    """
    get aliyun dns domain info
    return domain_records_id and domain_RR_ip dict
    """
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(domain)
    request.set_accept_format('json')

    try:
        response = client.do_action_with_exception(request)

    except Exception as e_message:
        return 'An error occurred! Error MSG: ' + str(e_message)

    else:
        response = response.decode()
        response_dict = json.JSONDecoder().decode(response)['DomainRecords']['Record']
        result_dict = {}
        for value in response_dict:
            if sub_domain == value['RR']:
                result_dict['RR'] = value['RR']
                result_dict['RecordId'] = value['RecordId']
                result_dict['Value'] = value['Value']
                break

        return result_dict


def update_domain_record(client, sub_domain, current_ip, record_id):
    """
    update aliyun dns ip address value
    """
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_RR(sub_domain)
    request.set_Value(current_ip)
    request.set_RecordId(record_id)
    request.set_Type('A')

    try:
        response = client.do_action_with_exception(request)
    except Exception as e_message:
        return 'An error occurred! Error MSG: ' + str(e_message)
    else:
        return response


def write_log(current_ip):
    """
    write update ip address log to file
    """
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(sys.path[0] + '/aliddns.log', 'a') as fd:
        fd.write('[' + time_now + ']' + ' ' + str(current_ip) + '\n')


def write_logs(current_ip):
    """
    write update ip address log to file
    """
    logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='[%Y-%m-%d %H:%M:%S]',
                filename='./aliyundns.log',
                filemode='a')
    return logging.info(current_ip)


def get_conf():
    """
    get info from config file
    """
    try:
        conf = open(sys.path[0] + '/config.json', 'r')
    except Exception as e:
        print('An error occurred, open config file fail! Error MSG: {}'.format(e))
        print('Script exit!')
        sys.exit(1)
    else:
        conf_dict = json.loads(conf.read())
        return conf_dict


if __name__ == '__main__':
    # 获取当前公网IP地址
    current_ip = get_public_ip()

    # 获取本地文件配置参数
    conf = get_conf()
    domain = conf['domain']
    sub_domain = conf['sub_domain']
    access_key_id = conf['access_key_id']
    access_key_secret = conf['access_key_secret']

    # 发起请求
    client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    domain_record = get_domain_record(client, domain, sub_domain)

    sub_domain_ip = domain_record['Value']
    record_id = domain_record['RecordId']

    if sub_domain_ip != current_ip:
        # 更新阿里云dns记录
        update_domain_record(client, sub_domain, current_ip, record_id)
        # 将当前公网ip写入到日志
        #write_log(current_ip)
        write_logs(current_ip)
