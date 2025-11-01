import os
import sqlite3
import sys

from argparser import ArgParse
from core import fullTable, queryTopRequestants, queryTopTargets, requestantQueries, updateDbase, runUserQuery, DB_PATH

VERSION = '2.0.0'

if __name__ == '__main__':
    args = ArgParse()
    args.parse(sys.argv[1:])

    if args.noArgs or args.help:
        print('bmdla: BMDNS Log Analyzer')
        print('usage: bmdla [OPTIONS]')
        print('options:')
        print('    -ds --db-structure              Show db strucure and exit')
        print('    -h  --help                      Show this message and exit')
        print('    -l  --limit N                   Limit output to N results')
        print('    -ft --full-table                Show full table')
        print('    -Q  --query QUERY               Run SQL query on dbase')
        print('    -rq --requestant-queries IP     Show queries for given requestant')
        print('    -td --top-domains               Show top domains')
        print('    -tr --top-requestants           Show top requestants')
        print('    -U  --update                    Update database with latest log')
        print('    -v  --verbose                   Verbose output while updating')
        print('    -V  --version                   Show version and exit')
        sys.exit(0)

    if args.version:
        print(f'BMDNS Log Analyzer v{VERSION}')
        sys.exit(1)

    if args.dbStructure:
        print(f'answer_type(id: int, description: text)')
        print(f'inspected_files(file: text)')
        print(f'bmdns_queries(id: int, ip: text, target: text, answer: int)')
        sys.exit(0)

    if args.update:
        if os.getuid() != 0:
            print('Error: database update requires root privilegies')
            sys.exit(1)

        try:
            updateDbase(args.verbose)

        except sqlite3.OperationalError:
            print('Error: database update requires root privilegies')
            sys.exit(1)

    if not os.path.exists(DB_PATH):
        print('Database does not exist. Run with `-U`')
        sys.exit(1)

    if args.topRequestants:
        queryTopRequestants(args.limit)

    elif args.topDomains:
        queryTopTargets(args.limit)

    elif args.fullTable:
        fullTable(args.limit)

    elif args.requestantQueries:
        requestantQueries(args.ip, args.limit)

    elif args.query is not None:
        runUserQuery(args.query, args.limit)