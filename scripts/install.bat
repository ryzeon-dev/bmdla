if not exists "src" (
    echo "Do not run installation script inside of `scripts` directory. Run it from the `bmdla` directory"
    exit /b 1
)

if not exists "%PROGRAMFILES%\bmdns" (
    echo "BMDLA requires bmdns to be installed"
    exit /b 1
)

python -m venv venv
set oldPath="%PATH%"
set PATH=".\venv\Scripts;%PATH%"

.\venv\Scripts\python.exe -m pip install pyinstaller
.\venv\Scripts\pyinstaller --onefile .\src\main.py --name bmdla

set PATH="%oldPath%"
mkdir .\bin

copy .\dist\bmdla.exe .\bin\bmdla.exe /Y
rmdir .\dist .\build .\venv /s /q

copy .\bin\bmdla.exe "%PROGRAMFILES%\bmdns\bin\bmdla.exe"