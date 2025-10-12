if [ ! -d "src" ]; then
  echo "Error: install script must be executed in the directory where `src` is"
  exit 1
fi

if [ "$(id -u)" != "0" ]; then
  echo "Error: install script must be executed as root"
  exit 1
fi

python3 -m venv venv
source ./venv/bin/activate
pip install pyinstaller
pyinstaller --onefile ./src/main.py --name bmdla
deactivate

mkdir -p ./bin
cp ./dist/bmdla ./bin/bmdla
rm -rf ./dist ./build ./bmdla.spec venv

cp ./bin/bmdla /usr/local/bin/
mkdir -p /usr/local/share/bmdns/dbase