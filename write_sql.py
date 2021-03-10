import json


def write_sql(wm, file, version):
    with open(wm, 'r', encoding='UTF-8') as worker_file:
        worker_file_content = json.load(worker_file)
    table = {
        'workerManager': worker_file_content,
    }
    content = json.dumps(table, separators=(',', ':')).replace('\\', '\\\\')
    sql = "UPDATE idc_config\n" \
          "SET `version` = {},\n" \
          "`config` = '{}'\n" \
          "WHERE\n" \
          "service_name = 'mix_streaming'\n" \
          "AND idc = '*';".format(version, content)
    with open(file, 'w', encoding='UTF-8') as out:
        out.write(sql)
