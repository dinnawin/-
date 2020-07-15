#!/bin/env /usr/local/python3.8/bin/python3
# -*- coding: utf8 -*-

import requests 
import json
import logging
from logging import Formatter
from jproperties import Properties
from multiprocessing import Process

logger = logging.getLogger('apollo_client')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('/tmp/configcenter_stdout.log',mode='a',encoding=None,delay=False)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


def get_configrations_from_url(
    config_server_url='http://124.206.6.52:30002',
    appid=None,
    clustername=None,
    namespaceName=None,
    releaseKey=None
):
    url = '{config_server_url}/configs/{appId}/{clusterName}/{namespaceName}?releaseKey={releaseKey}'.format(
            config_server_url=config_server_url,
            appId=appid,
            clusterName=clustername,
            namespaceName=namespaceName,
            releaseKey=releaseKey)
    
    try:
        data = requests.get(url=url)
        if data.status_code == 200:
            try:
                config_data = data.json()
                return config_data.get("configurations", None)
            except Exception:
                logger.info("type error, data is not a json type")      
    except Exception:
        logger.info('request error, url maybe wrong')

def write_properties(configs, file, path=None):
    
    if path is None:
        path = '/opt'
    pfile = Properties()
    d_file = path + '/' + file + '.properties'
    if configs is not None:
        for k, v in configs.items():
            pfile[k] = v
        with open(d_file, 'wb') as f:
            pfile.store(f, encoding='utf-8')

def multi_process(appid, namespace, cluster, config_url):
    try:
        config_items = get_configrations_from_url(
            appid=appid, 
            config_server_url=config_url, 
            clustername=cluster,
            namespaceName=namespace
        )
    except Exception as e:
        logger.info('{} {} {}'.format(app,namespace,e))

    write_properties(configs=config_items, file=namespace, path='/share/vems/config')                
    

if __name__ == '__main__':

    app_ns_dict = {
                    "bbpf-system": "bbpf-system",
                    "boss-api": "boss-api",
                    "discovery1": "discovery-discovery1",
                    "discovery2": "discovery-discovery2",
                    "discovery3": "discovery-discovery3",
                    #"local-system1": "local-system1",
                    #"local-system2": "local-system2",
                    "local-system": "local-system",
                    #"newbbpf-system": "newbbpf-system",
                    "ssms-finance": "ssms-finance",
                    #"sub-system-api": "sub-system-api",
                    #"sub-system": "sub-system",
                    "vems-adapter": "vems-adapter",
                    "gateway": "vems-api",
                    "vems-biometric": "vems-biometric",
                    #"vems-boss-api": "vems-boss-api",
                    "vems-boss-common-goods": "vems-boss-common-goods",
                    #"vems-boss-gd": "vems-boss-gd",
                    "vems-boss-goods-center": "vems-boss-goods-center",
                    #"vems-boss-grayapi": "vems-boss-grayapi",
                    "vems-boss-manager": "vems-boss-manager",
                    "vems-boss-open-way": "vems-boss-open-way",
                    "console-gateway": "vems-console-api",
                    "vems-content": "vems-content",
                    "vems-data-analysis": "vems-data-analysis",
                    "vems-dispatch": "vems-dispatch",
                    "vems-finance": "vems-finance",
                    "vems-intelligent-opendoor": "vems-intelligent-opendoor",
                    "vems-jtstatistic": "vems-jtstatistic",
                    "vems-lms": "vems-lms",
                    "vems-marketing": "vems-marketing",
                    "vems-membership": "vems-membership",
                    "vems-merchandise": "vems-merchandise",
                    "vems-miniprogrammall": "vems-miniprogrammall",
                    "vems-mqmanagement": "vems-mqmanagement",
                    "vems-onlinemall": "vems-onlinemall",
                    "vems-online": "vems-online",
                    "vems-open-api": "vems-open-api",
                    "vems-openapi": "vems-openapi",
                    "vems-openmanager": "vems-openmanager",
                    "operation-gateway": "vems-operation-api",
                    "vems-operation-manager": "vems-operation-manager",
                    "vems-operator": "vems-operator",
                    #"vems-order-new": "vems-order-new",
                    "vems-order": "vems-order",
                    "vems-pay": "vems-pay",
                    "vems-portal": "vems-portal",
                    "vems-presale": "vems-presale",
                    "vems-promotion": "vems-promotion",
                    #"vems-sale2": "vems-sale2",
                    "sale-gateway": "vems-sale-api",
                    "vems-sale": "vems-sale",
                    "vems-standard-order": "vems-standard-order",
                    "vems-standard-sale": "vems-standard-sale",
                    "vems-statistic": "vems-statistic",
                    "vems-tenant-center": "vems-tenant-center",
                    #"vems-third-party-communicate": "vems-third-party-communicate",
                    "vems-unicorn-finance": "vems-unicorn-finance",
                    "vems-unicorn-gateway": "vems-unicorn-gateway",
                    "vems-unicorn-job": "vems-unicorn-job",
                    "vems-unicorn-manage": "vems-unicorn-manage",
                    "vems-unicorn-pay": "vems-unicorn-pay",
                    "vems-unicorn-routing": "vems-unicorn-routing",
                    "vems-unicorn-transfer": "vems-unicorn-transfer",
                    "vems-valuation": "vems-valuation",
                    "vems-vendingmachine": "vems-vendingmachine",
                    "vems-wechat": "vems-wechat",
                    "vems-workorder-gd": "vems-workorder-gd",   
                    "vems-hanker": "vems-hanker",   
                        }
    while True: 
        process_list = []
        for app, ns in app_ns_dict.items():
            process = Process(target=multi_process, args=(app, ns, 'default', 'http://10.10.10.65:30002')) 
            process_list.append(process)
            process.start()
        for proce in process_list:
            proce.join()
#
#    multi_process('vems-pay','vems-pay','default','http://10.10.10.65:30002')
