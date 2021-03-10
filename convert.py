# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import json
import sys
from jsonschema import validate
import os
import operator


def check_schema(config_file, schema_file):
    with open(config_file, 'r', encoding='UTF-8') as configFile:
        config_file_content = json.load(configFile)
    with open(schema_file, 'r', encoding='UTF-8') as schemaFile:
        worker_schema_content = json.load(schemaFile)
    validate(config_file_content, schema=worker_schema_content)


def schemaContent(config_content, schema_file):
    with open(schema_file, 'r', encoding='UTF-8') as schemaFile:
        worker_schema_content = json.load(schemaFile)
    validate(config_content, schema=worker_schema_content)


def parse(workerFile, appFile, outputFile):
    # 校验 worker-manager.json 和 app-center.json 的格式
    work_schema_file = "worker_manager_config_schema.json"
    app_schema_file = "app_center_config_schema.json"
    check_schema(workerFile, work_schema_file)
    check_schema(appFile, app_schema_file)

    # 获取所有的vid
    # 获取worker-manager.json中所有出现过的vid
    with open(workerFile, 'r', encoding='UTF-8') as worker_file:
        worker_file_content = json.load(worker_file)
    workerConfigDetails = json.loads(worker_file_content["workerManager"]["workerConfig"])

    configdict = {}
    globalFeature = {}
    for key in workerConfigDetails:
        if type(workerConfigDetails[key]) == list:
            tmplist = workerConfigDetails[key]
            for i in range(len(tmplist)):
                configdict[tmplist[i]] = {}
        elif type(workerConfigDetails[key]) == dict:
            tmpdict = workerConfigDetails[key]
            for tmpkey in tmpdict:
                configdict[int(tmpkey)] = {}
        elif type(workerConfigDetails[key]) == bool:
            globalFeature[key] = workerConfigDetails[key]
        elif type(workerConfigDetails[key]) == str:
            globalFeature[key] = workerConfigDetails[key]

    # 获取app-center.json中所有出现过的vid
    with open(appFile, 'r', encoding='UTF-8') as app_file:
        app_file_content = json.load(app_file)
    vendorRegionDetails = app_file_content["vendor_region"]
    for i in range(len(vendorRegionDetails)):
        configdict[int(vendorRegionDetails[i]["vid"])] = {}

    # 初始化outputFile
    for vid_key in configdict:
        configdict[vid_key]["worker-manager"] = {}
        configdict[vid_key]["app-center"] = {}

    # 填写outputFile中vid的worker-manager信息
    for key in workerConfigDetails:
        if type(workerConfigDetails[key]) == list:
            tmplist = workerConfigDetails[key]
            listdict = {}
            listdict[key] = True
            for i in range(len(tmplist)):
                vid = tmplist[i]
                configdict[vid]["worker-manager"].update(listdict)
        elif type(workerConfigDetails[key]) == dict:
            tmpdict = workerConfigDetails[key]
            for tmpkey in tmpdict:
                dictdict = {}
                dictdict[key] = tmpdict[tmpkey]
                configdict[int(tmpkey)]["worker-manager"].update(dictdict)

    # 填写outputFile中vid的app-center信息
    for i in range(len(vendorRegionDetails)):
        vid = vendorRegionDetails[i]["vid"]
        del vendorRegionDetails[i]["vid"]
        configdict[vid]["app-center"].update(vendorRegionDetails[i])

    # 填写outputFile中worker-manage的全局信息
    configlist = []
    configlist.append(globalFeature)

    # 将outputFile中的vid对应的vid由dict格式转换为list格式
    for key_vid in configdict:
        tmpdict = {}
        tmpdict["vid"] = int(key_vid)
        dictdict = configdict[key_vid]
        tmpdict.update(dictdict)
        configlist.append(tmpdict)

    json_str = json.dumps(configlist, ensure_ascii=False, sort_keys=True)
    with open(outputFile, 'w', encoding='UTF-8') as f:
        f.write(json_str)
    print("parse worker-manager.json and app-center.json success, and generate total mix file success\n")


def generate(inputFile, workerFile, appFile, outWorker, outApp):
    # 校验 worker-manager.json的格式
    work_schema_file = "worker_manager_config_schema.json"
    app_schema_file = "app_center_config_schema.json"
    check_schema(workerFile, work_schema_file)
    check_schema(appFile, app_schema_file)

    # 校验 app-center.json的格式
    with open(workerFile, 'r', encoding='UTF-8') as worker_file:
        worker_file_content = json.load(worker_file)
    with open(appFile, 'r', encoding='UTF-8') as app_file:
        app_file_content = json.load(app_file)
    with open(inputFile, 'r', encoding='UTF-8') as f:
        content = json.load(f)

    workerConfig = {}
    appConfig = []
    globalFeature = content[0]

    # 获取 worker-manage.json 中的全局信息
    for key_feature in globalFeature:
        workerConfig[key_feature] = globalFeature[key_feature]
    del (content[0])

    # 获取inputFile中worker-manager的所有属性和app-center的相关信息
    for details in content:
        if (details["app-center"]):
            appdict = {}
            appdict["vid"] = details["vid"]
            appdict.update(details["app-center"])
            appConfig.append(appdict)
        if (details["worker-manager"]):
            for key_feature in details["worker-manager"]:
                if (type(details["worker-manager"][key_feature]) == bool):
                    workerConfig[key_feature] = []
                elif (type(details["worker-manager"][key_feature]) == int):
                    workerConfig[key_feature] = {}
                elif (type(details["worker-manager"][key_feature]) == float):
                    workerConfig[key_feature] = {}
    sorted_appConfig = sorted(appConfig, key=operator.itemgetter('vid'))
    # 获取inputFile中worker-manager属性的具体信息
    for details in content:
        if (details["worker-manager"]):
            for key_feature in details["worker-manager"]:
                if (type(details["worker-manager"][key_feature]) == bool):
                    workerConfig[key_feature].append(int(details["vid"]))
                elif (type(details["worker-manager"][key_feature]) == int):
                    tmpdict = {}
                    tmpdict[details["vid"]] = details["worker-manager"][key_feature]
                    workerConfig[key_feature].update(tmpdict)
                elif (type(details["worker-manager"][key_feature]) == float):
                    tmpdict = {}
                    tmpdict[details["vid"]] = details["worker-manager"][key_feature]
                    workerConfig[key_feature].update(tmpdict)

    # 校验新生成的worker-manager.json的格式,如果正确，就输出worker-manager.json
    json_str = json.dumps(workerConfig, separators=(',', ':'), sort_keys=True)
    worker_file_content["workerManager"]["workerConfig"] = json_str
    print(json_str)
    schemaContent(worker_file_content, work_schema_file)
    json_workerConfig = json.dumps(worker_file_content, ensure_ascii=False, sort_keys=True)
    with open(outWorker, 'w', encoding='UTF-8') as f:
        f.write(json_workerConfig)

    # 校验新生成的app-center.json的格式,如果正确，就输出app-center.json
    app_file_content["vendor_region"] = sorted_appConfig
    schemaContent(app_file_content, app_schema_file)
    json_appConfig = json.dumps(app_file_content, ensure_ascii=False, sort_keys=True)
    with open(outApp, 'w', encoding='UTF-8') as f:
        f.write(json_appConfig)
    print("parse total mix file success, and generate worker-manager.json and app-center.json success\n")
