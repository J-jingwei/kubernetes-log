#！/usr/bin/env python3
# -*- coding: utf-8 -*-
'''通过输入pod名，取出所需的所有pod'''

import urllib3
from kubernetes import client
from kubernetes.client.rest import ApiException

urllib3.disable_warnings()


def grep_pod(Token, APISERVER, namespace, LABEL, LABEL2):
    try:
        pod_num = 0
        pod_names = []

        configuration = client.Configuration()
        configuration.host = APISERVER
        configuration.verify_ssl = False
        configuration.api_key = {'authorization': 'Bearer ' + Token}
        client.Configuration.set_default(configuration)

        api_instance = client.CoreV1Api()
        api_response = api_instance.list_namespaced_pod(namespace)
        pod_list = api_response.items
        for i in pod_list:
            # pod名字
            pod_name = i.metadata.name
            # 镜像版本
            # image_version = i.status.container_statuses[0].image.split(':')[1]
            # pod状态
            pod_status = i.status.phase
            pod_time = i.status.start_time
            pod_message = pod_status + '=>' + str(pod_time).split('+')[0]
            # pod所在宿主机
            # pod_host = i.status.host_ip
            if LABEL in pod_name:
                if LABEL2 in pod_name:
                    name_status = {pod_name: pod_message}
                    pod_names.append(name_status)
                    pod_num += 1
        return pod_names
    except ApiException as e:
        return 'search pod error'


def main(Token, APISERVER, namespace, LABEL):
    # 使用
    grep_pod(Token, APISERVER, namespace, LABEL, LABEL2)
