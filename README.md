
#安装依赖
`pip install -r requirements.txt`

#具体说明
**查看命令行用法 **
`python main.py -h`

## parse用法 ##
**将worker-manager.json中的workerConfig属性和app-center.json中的vendor_region属性汇总到result.json文件中，方便根据vid进行修改####将worker-manager.json中的workerConfig属性和app-center.json中的vendor_region属性汇总到result.json文件中，方便根据vid进行修改**
`python main.py parse -iw worker-manager.json -ia app-center.json -o result.json`

## generate用法 ##
**将修改后的结果重新写入新的worker-manager.json和app-center.json中**
`python main.py generate -i result.json -iw worker-manager.json -ia app-center.json -ow worker-manager1.json -oa app-center1.json`




