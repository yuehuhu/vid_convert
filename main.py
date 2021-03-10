import argparse

from convert import parse
from convert import generate

#
#  parse:
#      python3 main.py parse \
#      -iw input worker-manager.json \
#      -ia input app-center.json \
#      -o output.json
#
#  generate:
#      python3 main.py generate \
#      -i input.json \
#      -iw input worker-manager.json \
#      -ia input app-center.json \
#      -ow output worker-manager.json \
#      -oa output app-center.json
from write_sql import write_sql

parser = argparse.ArgumentParser(
    prog='converter',
    description='parse or generate config files'
)

parser.add_argument(
    '-iw',
    dest='input_worker',
    default='worker-manager.json',
    help='source worker manager config file'
)

parser.add_argument(
    '-ia',
    dest='input_app',
    default='app-center.json',
    help='source app center config file'
)

sub_parser = parser.add_subparsers(
    dest="sub",
)

parser_parser = sub_parser.add_parser('parse')
parser_parser.add_argument(
    '-o',
    dest='output',
    default='config.json',
    help='vid config files'
)

generate_parser = sub_parser.add_parser('generate')
generate_parser.add_argument(
    '-i',
    dest='input',
    default='config.json',
    help='vid config file'
)

generate_parser.add_argument(
    '-ow',
    dest='output_worker',
    default='new-worker-manager.json',
    help='new worker manager config file'
)

generate_parser.add_argument(
    '-oa',
    dest='output_app',
    default='new-app-center.json',
    help='new app center config file'
)

sql_parser = sub_parser.add_parser('sql')
sql_parser.add_argument(
    '-os',
    dest='out_sql',
    default='update.sql',
    help='output sql file'
)

sql_parser.add_argument(
    '-v',
    dest='sql_version',
    required=True,
    help='idc config version'
)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.sub is None:
        parser.print_help()
        exit(0)
    if args.sub == "parse":
        parse(args.input_worker, args.input_app, args.output)
    elif args.sub == "generate":
        generate(args.input, args.input_worker, args.input_app, args.output_worker, args.output_app)
    elif args.sub == 'sql':
        write_sql(args.input_worker, args.out_sql, args.sql_version)
