#！/usr/bin/env python3
# -*- coding: utf-8 -*-
'''通过修改pod关键词，以及log中的关键字，取出所需的所有pod log'''

import urllib3
from kubernetes import client
from kubernetes.client.rest import ApiException
import list_namespace_pod

# 忽略未受信证书告警
urllib3.disable_warnings()

def pod_log(Token, APISERVER, podman, namespace, keyword, keyword2, scope):
    try:
        configuration = client.Configuration()
        configuration.host = APISERVER
        configuration.verify_ssl = False
        configuration.api_key = {'authorization': 'Bearer ' + Token}
        client.Configuration.set_default(configuration)

        api_instance = client.CoreV1Api()
        api_response = api_instance.read_namespaced_pod_log(name=podman, namespace=namespace)
        api_dataline = api_response.splitlines()
        # 过滤关键字，得到索引确认位置，然后切片列表
        logs = []
        for i in api_dataline:
            if keyword in i:
                if keyword2 in i:
                    num = api_dataline.index(i)
                    num_a = num - scope
                    num_b = num + scope + 1
                    if num_a < 0:
                        num_a = 0
                    for t in api_dataline[num_a:num_b]:
                        logs.append(t)
        return logs
    except ApiException as e:
        return "Exception when calling CoreV1Api->list_pod_log: %s\n" % e


def main(Token, APISERVER, namespace, LABEL, LABEL2, keyword, keyword2, scope):
    # 调用取出关键词pod
    pod_names = list_namespace_pod.grep_pod(Token, APISERVER, namespace, LABEL, LABEL2)
    # 将各个pod循环，得到全部日志
    logAll = []
    for i in pod_names:
        for k, v in i.items():
            # 过滤日志,并列表收集
            podOne = pod_log(Token, APISERVER, k, namespace, keyword, keyword2, scope)
            for l in podOne:
                logAll.append(l)
    return logAll
