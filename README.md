<p align="center">
<img alt="Version Badge" src="https://img.shields.io/badge/dev--version-v2.0.0-16a085">
<img alt="Version Badge" src="https://img.shields.io/badge/release-v2.0.0-16a085">
<img alt="License Badge" src="https://img.shields.io/github/license/ryzeon-dev/bmdla?color=16a085">
<img alt="Language Badge" src="https://img.shields.io/badge/python3-16a085?logo=python&logoColor=16a085&labelColor=5a5a5a">
</p>

# BMDNS Log Analyzer
Log analysis utility for [BMDNS](https://github.com/ryzeon-dev/bmdns)

## Supported OS
Right now, BMDLA only supports GNU/Linux and Windows systems

## OS Requirements
BMDLA requires `python3 python3-venv python3-pip python3-sqlite3` packages to be installed in order to compile

## Install
#### Linux
Run the installation script as root, from the main `bmdla` directory:
```commandline
sudo bash ./scripts/install.sh
```

#### Windows
Run the installation script as an administrator, from the main `bmdla` directory:
```commandline 
.\scripts\install.bat
```

## Uninstall
#### Linux
Run the uninstallation script as root, from the main `bmdla` directory:
```commandline
sudo bash ./scripts/uninstall.sh
```

#### Windows
Run the uninstallation script as an administrator, from the main `bmdla` directory:
```commandline
.\scripts\uninstall.bat
```

## Usage
```
~ $ bmdla --help
bmdla: BMDNS Log Analyzer
usage: bmdla [OPTIONS]
options:
    -ds --db-structure              Show db strucure and exit
    -h  --help                      Show this message and exit
    -l  --limit N                   Limit output to N results
    -ft --full-table                Show full table
    -Q  --query QUERY               Run SQL query on dbase
    -rq --requestant-queries IP     Show queries for given requestant
    -td --top-domains               Show top domains
    -tr --top-requestants           Show top requestants
    -U  --update                    Update database with latest log
    -v  --verbose                   Verbose output while updating
    -V  --version                   Show version and exit
```