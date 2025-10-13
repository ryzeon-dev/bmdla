import sqlite3
import os
import re
import sys

BMDNS_DIR = '/usr/local/share/bmdns/'
DB_PATH = '/usr/local/share/bmdns/dbase/bmdns.db'
LOG_DIR = '/usr/local/share/bmdns/'

class ANSWER_TYPE:
    ROOT_SERVER = 1
    STATIC = 2
    CACHED = 3
    REFUSAL = 4

class Request:
    def __init__(self, id, requestant, target):
        self.id = id
        self.requestant = requestant
        self.requestantIp = self.requestant.split(':')[0]
        self.requestantPort = self.requestant.split(':')[1]
        self.target = target
        self.answerType = 0

    def __repr__(self):
        return f'Request({self.id}@{self.requestant} ; target: {self.target} ; answer: {self.answerType})'

def createDbase():
    if not os.path.exists(BMDNS_DIR):
        print('Error: bmdns appears to not be installed')
        sys.exit(1)

    dbaseDir = os.path.join(BMDNS_DIR, 'dbase')
    if not os.path.exists(dbaseDir):
        os.mkdir(dbaseDir)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("create table answer_type (id integer primary key,description text)")

    cursor.execute("insert into answer_type(description) values ('root server')")
    cursor.execute("insert into answer_type(description) values ('static')")

    cursor.execute("insert into answer_type(description) values ('cached')")
    cursor.execute("insert into answer_type(description) values ('refusal')")

    cursor.execute("create table inspected_files (file text primary key)")
    cursor.execute("create table bmdns_queries (id integer primary key, ip text, target text, answer int)")

    connection.commit()
    cursor.close()
    connection.close()

def inspectLogFile(filePath):
    logs = []
    unterminated = {
        # identifier : request
    }

    with open(filePath, 'r') as file:
        log = file.read()

    for line in log.split('\n'):
        if not line or 'Error: ' in line:
            continue

        chunks = line.split('|')
        requestId = chunks[1].strip()
        requestant = re.search(r'(([0-9]{1,3}\.){3}[0-9]{1,3}:\d{1,5})', chunks[2]).group(1)

        identifier = f'{requestId}@{requestant}'

        if line.startswith('[!]'):
            request = chunks[2].split(' ')
            target = request[-1]

            unterminated[identifier] = Request(requestId, requestant, target)

        elif line.startswith('[*]'):
            text = chunks[2]

            if 'root server answer' in text:
                answerType = ANSWER_TYPE.ROOT_SERVER

            elif 'giving static answer' in text or 'giving static vlan' in text:
                answerType = ANSWER_TYPE.STATIC

            elif 'giving cached' in text:
                answerType = ANSWER_TYPE.CACHED

            logRequest = unterminated.pop(identifier)
            logRequest.answerType = answerType

            logs.append(logRequest)

        elif line.startswith('[x]'):
            logRequest = unterminated.pop(identifier)
            logRequest.answerType = ANSWER_TYPE.REFUSAL

            logs.append(logRequest)

    return logs

def updateDbase():
    if not os.path.exists(DB_PATH):
        createDbase()

    connection = sqlite3.connect(DB_PATH)
    dbase = connection.cursor()

    dbase.execute("select distinct file from inspected_files")
    inspectedFiles = set(row[0] for row in dbase.fetchall())

    for file in os.listdir(LOG_DIR):
        if file in inspectedFiles:
            continue

        if not re.fullmatch(r'^bmdns_\d{4}-\d{1,2}-\d{1,2}_\d{1,2}-\d{1,2}-\d{1,2}\.log$', file) and file != 'bmdns.log':
            continue

        fileLog = inspectLogFile(os.path.join(LOG_DIR, file))
        if file != 'bmdns.log':
            dbase.execute(f"insert into inspected_files(file) values ('{file}')")

        for entry in fileLog:
            ip = entry.requestantIp
            target = entry.target

            answer = entry.answerType
            dbase.execute(f"insert into bmdns_queries(ip, target, answer) values ('{ip}', '{target}', {answer});")

    connection.commit()
    dbase.close()
    connection.close()

def runQuery(query, limit):
    try:
        connection = sqlite3.connect(DB_PATH)

    except sqlite3.OperationalError:
        print(f'Error: database file has not been created yet. Rerun with `-U` or `--update`')
        sys.exit(1)

    cursor = connection.cursor()

    if limit != -1:
        query += f' limit {limit};'

    else:
        query += ';'

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def checkRows(rows):
    if not rows:
        print('Error: empty database. Run with `-U` or `--update`')
        sys.exit(1)

def queryTopRequestants(limit):
    query = "select distinct ip, count(id) from bmdns_queries group by ip order by count(id) desc"
    rows = runQuery(query, limit)

    checkRows(rows)
    printFmtRows(rows if limit == -1 else rows[:limit])

def queryTopTargets(limit):
    query = "select distinct target, count(id) from bmdns_queries group by target order by count(id) desc"
    rows = runQuery(query, limit)

    checkRows(rows)
    printFmtRows(rows if limit == -1 else rows[:limit])

def fullTable(limit):
    query = "select bq.ip, bq.target, at.description FROM bmdns_queries as bq join answer_type as at on bq.answer = at.id"
    rows = runQuery(query, limit)

    checkRows(rows)
    rows.insert(0, ('Sender', 'Target', 'Answer'))
    printFmtRows(rows)

def requestantQueries(ip, limit):
    query = f"select distinct bq.ip, bq.target, count(bq.target) FROM bmdns_queries as bq where bq.ip='{ip}' group by bq.ip, bq.target order by count(bq.target) desc"
    rows = runQuery(query, limit)

    checkRows(rows)
    rows.insert(0, ('Sender', 'Target', 'Count'))
    printFmtRows(rows)

def _detectIllegalQuery(query):
    query = query.lower()

    insert = False
    delete = False
    update = False
    drop = False
    create = False

    last = None

    for chunk in query.split(' '):
        if not chunk.strip():
            continue

        if chunk == 'into' and last == 'insert':
            insert = True

        elif chunk == 'from' and last == 'delete':
            delete = True

        elif chunk == 'table' and last == 'create':
            create = True

        elif chunk == 'table' and last == 'drop':
            drop = True

        elif chunk == 'update':
            update = True

        last = chunk

    return insert or delete or create or update or drop

def runUserQuery(query, limit):
    if _detectIllegalQuery(query):
        print('Error: only `SELECT` queries can be run')
        sys.exit(1)

    try:
        rows = runQuery(query, limit)

    except sqlite3.OperationalError as e:
        print(f'Error: `{e}`')
        sys.exit(1)

    if rows:
        printFmtRows(rows)

def printFmtRows(rows):
    colMaxLen = [0] * len(rows[0])
    for row in rows:
        for index, col in enumerate(row):
            colMaxLen[index] = max(colMaxLen[index], len(str(col)))

    for row in rows:
        print('| ', end='')
        chunks = []

        for i in range(len(row)):
            value = row[i]
            padding = colMaxLen[i]
            chunks.append(str(value).ljust(padding))

        print(' | '.join(chunks), end='')
        print(' |')