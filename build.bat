@echo off
setlocal

where python >nul 2>nul
if errorlevel 1 (
    echo Python nao encontrado. Instale o Python em https://www.python.org/downloads/
    echo e marque a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
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
