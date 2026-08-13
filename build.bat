@echo off
setlocal

set "MIN_MAJOR=3"
set "MIN_MINOR=12"
set "PYCMD="

for %%C in (python python3 py) do (
    if not defined PYCMD call :check_python %%C
)

if not defined PYCMD (
    echo.
    echo Nao foi possivel encontrar um Python valido ^(minimo %MIN_MAJOR%.%MIN_MINOR%^) via "python", "python3" ou "py".
    echo Instale o Python em https://www.python.org/downloads/ e marque "Add Python to PATH".
    pause
    exit /b 1
)

echo Usando "%PYCMD%".

if not exist .venv (
    echo Criando ambiente virtual...
    %PYCMD% -m venv .venv
)

echo Instalando dependencias...
.venv\Scripts\python.exe -m pip install --upgrade pip >nul
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Falha ao instalar as dependencias.
    pause
    exit /b 1
)

echo Gerando executavel...
.venv\Scripts\python.exe -m PyInstaller --onedir --windowed --noconfirm --name RNC_Concat gui.py
if errorlevel 1 (
    echo Falha ao gerar o executavel.
    pause
    exit /b 1
)

echo.
echo Concluido! O executavel esta em dist\RNC_Concat\RNC_Concat.exe
pause
exit /b 0

:check_python
set "CANDIDATE=%~1"

where %CANDIDATE% >nul 2>nul
if errorlevel 1 (
    echo - %CANDIDATE%: comando nao encontrado.
    goto :eof
)

for /f "tokens=2 delims= " %%V in ('%CANDIDATE% --version 2^>^&1') do set "VERSION=%%V"

set "VMAJOR="
set "VMINOR="
for /f "tokens=1,2 delims=." %%A in ("%VERSION%") do (
    set "VMAJOR=%%A"
    set "VMINOR=%%B"
)

echo %VMAJOR%|findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo - %CANDIDATE%: nao foi possivel identificar a versao do Python ^(retorno: %VERSION%^).
    goto :eof
)
echo %VMINOR%|findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo - %CANDIDATE%: nao foi possivel identificar a versao do Python ^(retorno: %VERSION%^).
    goto :eof
)

if %VMAJOR% GTR %MIN_MAJOR% set "PYCMD=%CANDIDATE%"
if %VMAJOR% EQU %MIN_MAJOR% if %VMINOR% GEQ %MIN_MINOR% set "PYCMD=%CANDIDATE%"

if defined PYCMD (
    echo - %CANDIDATE%: versao %VERSION% OK.
) else (
    echo - %CANDIDATE%: versao %VERSION% encontrada, requer ^>= %MIN_MAJOR%.%MIN_MINOR%.
)
goto :eof
