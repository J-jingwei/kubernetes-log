#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''pod status '''
__author__ = 'jiangjw'

import list_namespace_pod

def podStatus(Token, APISERVER, namespace, LABEL, LABEL2):
    pod_names = list_namespace_pod.grep_pod(Token, APISERVER, namespace, LABEL, LABEL2)
    statusValue = []
    for i in pod_names:
        for k,v in i.items():
            statusValue.append(v)
    return statusValue