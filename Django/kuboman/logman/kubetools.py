#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''通过输入server，取出所需的所有pod'''

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'books.settings'  # 配置系统变量
import django

import urllib3
import datetime
import traceback
import socket
from kubernetes import client
from kubernetes.client.rest import ApiException

django.setup()


class FilterBundle():
    def __init__(self, token, apiserver, namespace, server, scope=0):
        self.token = token
        self.apiserver = apiserver
        self.namespace = namespace
        self.server = server
        self.scope = scope

    def initSetting(self):
        urllib3.disable_warnings()
        configuration = client.Configuration()
        configuration.host = self.apiserver
        configuration.verify_ssl = False
        configuration.api_key = {'authorization': 'Bearer ' + self.token}
        client.Configuration.set_default(configuration)
        return client

    def telnet(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(2)
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except:
            return False

    def hostStatus(self, host):
        try:
            api_instance = self.initSetting().CoreV1Api()
            api_response = api_instance.list_node()
            for h in api_response.items:
                svc_ip = h.status.addresses[0].address
                if host in svc_ip:
                    host_status = h.status.conditions[3].status
                    return host_status
        except ApiException as e:
            traceback.print_exc(e)

    def filterSvc(self):
        try:
            api_instance = self.initSetting().CoreV1Api()
            api_response = api_instance.list_namespaced_service(self.namespace)
            svc_list = api_response.items
            for s in svc_list:
                # svc name
                svc_name = s.metadata.name
                if self.server in svc_name:
                    # print(s)
                    svc_type = s.spec.type
                    svc_ip = s.spec.cluster_ip
                    svc_port = s.spec.ports[0].port
                    svc_message = "http://x.x.x.x:8080" + s.metadata.self_link
                    if self.namespace == 'default':
                        svc_bundle = {'svc_name': svc_name, 'svc_type': svc_type, 'svc_ip': svc_ip,
                                      'svc_port': svc_port,
                                      'socket_status': "阿里云暂不支持检测", 'svc_message': "暂不支持阿里云"}
                    else:
                        svc_bundle = {'svc_name': svc_name, 'svc_type': svc_type, 'svc_ip': svc_ip,
                                      'svc_port': svc_port,
                                      'socket_status': self.telnet(svc_ip, svc_port), 'svc_message': svc_message}
                    yield svc_bundle
        except ApiException as e:
            traceback.print_exc(e)

    def readSvc(self):
        try:
            api_instance = self.initSetting().CoreV1Api()
            api_response = api_instance.read_namespaced_service(name=self.server, namepace=self.namespace)
            svc_list = api_response.items
            # for s in svc_list:
            #     # svc name
            svc_name = svc_list.metadata.name
            if self.server in svc_name:
                # print(s)
                svc_type = svc_list.spec.type
                svc_ip = svc_list.spec.cluster_ip
                svc_port = svc_list.spec.ports[0].port
                svc_message = "http://x.x.x.x:8080" + s.metadata.self_link
                if self.namespace == 'default':
                    svc_bundle = {'svc_name': svc_name, 'svc_type': svc_type, 'svc_ip': svc_ip,
                                  'svc_port': svc_port,
                                  'socket_status': "阿里云暂不支持检测", 'svc_message': "暂不支持阿里云"}
                else:
                    svc_bundle = {'svc_name': svc_name, 'svc_type': svc_type, 'svc_ip': svc_ip,
                                  'svc_port': svc_port,
                                  'socket_status': self.telnet(svc_ip, svc_port), 'svc_message': svc_message}
                yield svc_bundle
        except ApiException as e:
            traceback.print_exc(e)

    def filterPod(self):
        try:
            api_instance = self.initSetting().CoreV1Api()
            api_response = api_instance.list_namespaced_pod(self.namespace)
            pod_list = api_response.items
            for p in pod_list:
                # pod名字
                pod_name = p.metadata.name
                # print(self.server)
                if self.server in pod_name or self.server[:-6] in pod_name:
                    # print(i)
                    # 镜像版本
                    image_version = p.status.container_statuses[0].image.split(':')[1]
                    # pod状态
                    pod_status = p.status.phase
                    pod_time = p.status.start_time + datetime.timedelta(hours=8)
                    # pod所在宿主机
                    pod_host = p.status.host_ip
                    pod_ip = p.status.pod_ip
                    log_url = "http://x.x.x.x:8080/api/v1/namespaces/{}/pods/{}/log".format(self.namespace,
                                                                                                 pod_name)
                    if self.namespace == 'default':
                        pod_bundle = {'pod_name': pod_name, 'status': pod_status, 'pod_ip': pod_ip,
                                      'version': image_version,
                                      'starttime': str(pod_time).split('+')[0], 'host': pod_host,
                                      'host_status': "阿里云暂不支持检测", "log_url": "暂不支持阿里云"}
                    else:
                        pod_bundle = {'pod_name': pod_name, 'status': pod_status, 'pod_ip': pod_ip,
                                      'version': image_version,
                                      'starttime': str(pod_time).split('+')[0], 'host': pod_host,
                                      'host_status': self.hostStatus(pod_host), "log_url": log_url}
                    yield pod_bundle
        except ApiException as e:
            traceback.print_exc(e)

    def filterIng(self):
        try:
            api_instance = self.initSetting().ExtensionsV1beta1Api()
            api_response = api_instance.list_namespaced_ingress(namespace=self.namespace)
            ing_list = api_response.items
            for i in ing_list:
                # pod名字
                ing_http = i.spec.rules[0].http.paths
                for s in ing_http:
                    ing_svc = s.backend.service_name
                    # print(self.server)
                    if self.server in ing_svc:
                        ing_name = i.metadata.name
                        ing_domain = i.spec.rules[0].host
                        ing_port = s.backend.service_port
                        ing_path = "http://" + ing_domain + s.path
                        ing_msg = "http://192.168.1.100:8080" + i.metadata.self_link
                        if self.namespace == 'default':
                            ing_msg = "暂不支持阿里云"
                        else:
                            ing_msg = "http://192.168.1.100:8080" + i.metadata.self_link
                        ing_bundle = {"ing_name": ing_name, "ing_domain": ing_domain, "ing_svc": ing_svc,
                                      "ing_port": ing_port, "ing_path": ing_path, "ing_msg": ing_msg}
                        yield ing_bundle
        except ApiException as e:
            traceback.print_exc(e)

    def filterPath(self, ingress_name, ingress_path):
        try:
            api_instance = self.initSetting().ExtensionsV1beta1Api()
            api_response = api_instance.read_namespaced_ingress(name=ingress_name, namespace=self.namespace)
            ing_http = api_response.spec.rules[0].http.paths
            for s in ing_http:
                ing_path = s.path
                if ingress_path == ing_path:
                    ing_svc = s.backend.service_name
                    ing_name = api_response.metadata.name
                    ing_domain = api_response.spec.rules[0].host
                    ing_port = s.backend.service_port
                    ing_path = "http://" + ing_domain + s.path
                    ing_msg = "http://x.x.x.x:8080" + api_response.metadata.self_link
                    ing_bundle = {"ing_name": ing_name, "ing_domain": ing_domain, "ing_svc": ing_svc,
                                  "ing_port": ing_port, "ing_path": ing_path, "ing_msg": ing_msg}
                    self.server = ing_svc
                    yield ing_bundle
        except ApiException as e:
            traceback.print_exc(e)


class ToolsBundle():
    def __init__(self, serverName='', urlPath='', envName='sit'):
        if envName == 'release':
            self.apiserver = 'https://x.x.x.x:6443'
            self.Token = 'token,自行通过命令行拿'
            self.envName = 'default'
        else:
            self.Token = 'token,自行通过命令行拿'
            self.apiserver = 'https://x.x.x.x:6443'
            self.envName = envName
        self.serverName = serverName
        self.urlPath = urlPath

        self.tools = FilterBundle(token=self.Token, apiserver=self.apiserver, server=self.serverName,
                                  namespace=self.envName)

    def pod(self):
        pod_bundle = self.tools.filterPod()
        return pod_bundle

    def svc(self):
        svc_bundle = self.tools.filterSvc()
        return svc_bundle

    def ing(self):
        ing_bundle = self.tools.filterIng()
        return ing_bundle

    def ingpath(self):
        dev_ingdata = {"域名":"ingressname",自行通过命令行用awk快速生成一下}
        sit_ingdata = {"域名":"ingressname",自行通过命令行用awk快速生成一下}
        release_ingdata = {"域名":"ingressname",自行通过命令行用awk快速生成一下}
        if self.envName == 'sit':
            ing_name = sit_ingdata.get(self.urlPath.split('/')[2])
            ing_path = "/" + self.urlPath.split('/')[3]
        elif self.envName == 'default':
            ing_name = release_ingdata.get(self.urlPath.split('/')[2])
            ing_path = "/" + self.urlPath.split('/')[3]
        else:
            ing_name = dev_ingdata.get(self.urlPath.split('/')[2])
            ing_path = "/" + self.urlPath.split('/')[3]

        ingpath_bundle = self.tools.filterPath(ingress_name=ing_name, ingress_path=ing_path)
        return ingpath_bundle

    def read(self):
        return self.tools.readSvc()