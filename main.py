import os
import argparse
import json
from convert import parse
from convert import generate
#  subcomand
#  -a app center config
#  -w worker manager config
#  -o output file
#  -i input file
#
#  parse:
#      format:  python3 main.py parse -iw input worker-manager.json -ia input app-center.json -o output.json
#      example: python3 main.py parse -iw worker-manager.json -ia app-center.json -o result.json

#  generate:
#     format:  python3 main.py generate -i input.json -iw input worker-manager.json -ia input app-center.json -ow output worker-manager.json -oa output app-center.json
#     example: python3 main.py generate -i result.json -iw worker-manager.json -ia app-center.json -ow worker-manager1.json -oa app-center1.json

parser = argparse.ArgumentParser(
    prog='converter',
    formatter_class=argparse.RawTextHelpFormatter,
    description='parse or generate config files'
)

parser.add_argument(
    'usage',
    help='（input parse or generate）\n \
    parse:\n \
        format:  python3 main.py parse -iw input worker-manager.json -ia input app-center.json -o output.json\n \
        example: python3 main.py parse -iw worker-manager.json -ia app-center.json -o result.json\n \
    generate:\n \
        format:  python3 main.py generate -i input.json -iw input worker-manager.json -ia input app-center.json -ow output worker-manager.json -oa output app-center.json\n \
        example: python3 main.py generate -i result.json -iw worker-manager.json -ia app-center.json -ow worker-manager1.json -oa app-center1.json'
)

parser.add_argument(
    '-iw',
    dest='input_worker',
    help='input worker-manager-config-file'
)

parser.add_argument(
    '-ia',
    dest='input_app',
    help='input app-center-config-file'
)

parser.add_argument(
    '-o',
    dest='output',
    help='output.json'
)

parser.add_argument(
    '-i',
    dest='input',
    help='input.json'
)

parser.add_argument(
    '-ow',
    dest='output_worker',
    help='output worker-manager-config-file'
)

parser.add_argument(
    '-oa',
    dest='output_app',
    help='output app-center-config-file'
)


if __name__ == "__main__":
    args = parser.parse_args()
    if(args.usage=="parse"):
        parse(args.input_worker,args.input_app,args.output)
    elif(args.usage=="generate"):
        generate(args.input,args.input_worker,args.input_app,args.output_worker,args.output_app)
       

