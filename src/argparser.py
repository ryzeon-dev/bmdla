import sys

class ArgParse:
    def __init__(self):
        self.update = False
        self.topRequestants = False
        self.topDomains = False
        self.fullTable = False
        self.requestantQueries = False
        self.ip = None
        self.query = None
        self.limit = -1

        self.dbStructure = False
        self.noArgs = True
        self.help = False
        self.version = False
        self.verbose = False

    def parse(self, args):
        if len(args) == 0:
            return

        self.noArgs = False

        index = 0
        while index < len(args):
            arg = args[index]

            if arg.startswith('--'):
                if arg == '--update':
                    self.update = True

                elif arg == '--top-requestants':
                    self.topRequestants = True

                elif arg == '--top-domains':
                    self.topDomains = True

                elif arg == '--full-table':
                    self.fullTable = True

                elif arg == '--requestant-queries':
                    self.requestantQueries = True
                    index += 1

                    if index == len(args):
                        print('Expecting IP after `--requestant-queries`')
                        sys.exit(1)

                    self.ip = args[index]

                elif arg == '--limit':
                    index += 1

                    if index == len(args):
                        print('Expecting a value after `--limit`')
                        sys.exit(1)

                    arg = args[index]
                    if not arg.isnumeric():
                        print('Expecting a positive integer value after `--limit`')
                        sys.exit(1)

                    self.limit = int(arg)

                elif arg == '--help':
                    self.help = True

                elif arg == '--query':
                    index += 1

                    if index == len(args):
                        print('Expecting a string after `--query`')
                        sys.exit(1)

                    self.query = args[index]

                elif arg == '--db-structure':
                    self.dbStructure = True

                elif arg == '--version':
                    self.version = True

                elif arg == '--verbose':
                    self.verbose = True

                else:
                    print(f'Unexpected argument: `{arg}`')

            elif arg.startswith('-'):
                if arg == '-U':
                    self.update = True

                elif arg == '-tr':
                    self.topRequestants = True

                elif arg == '-td':
                    self.topDomains = True

                elif arg == '-ft':
                    self.fullTable = True

                elif arg == '-rq':
                    self.requestantQueries = True
                    index += 1

                    if index == len(args):
                        print('Expecting IP after `-rq`')
                        sys.exit(1)

                    self.ip = args[index]

                elif arg == '-l':
                    index += 1

                    if index == len(args):
                        print('Expecting a value after `-l`')
                        sys.exit(1)

                    arg = args[index]
                    if not arg.isnumeric():
                        print('Expecting a positive integer value after `-l`')
                        sys.exit(1)

                    self.limit = int(arg)

                elif arg == '-h':
                    self.help = True

                elif arg == '-Q':
                    index += 1

                    if index == len(args):
                        print('Expecting a string after `--query`')
                        sys.exit(1)

                    self.query = args[index]

                elif arg == '-ds':
                    self.dbStructure = True

                elif arg == '-V':
                    self.version = True

                elif arg == '-v':
                    self.verbose = True

                else:
                    print(f'Unexpected argument: `{arg}`')
                    sys.exit(1)

            else:
                print(f'Unexpected argument: `{arg}`')
                sys.exit(1)

            index += 1