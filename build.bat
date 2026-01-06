@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul

:: ============================================================
:: 🚀 Build completo do GameLabs
:: ============================================================
set "APP_NAME=GameLabs"

:: Define o diretório base como o diretório onde este arquivo .bat está
set "BASE_DIR=%~dp0"
:: Remove a barra invertida final, se houver
if "%BASE_DIR:~-1%"=="\" set "BASE_DIR=%BASE_DIR:~0,-1%"

cd /d "%BASE_DIR%"

echo.
echo ============================================================
echo   🚀 Iniciando build do %APP_NAME%...
echo ============================================================
echo   📂 Diretório do projeto: %BASE_DIR%
echo.

:: --- Caminhos dos Arquivos ---
set "ICON_PATH=%BASE_DIR%\app\assets\icon.ico"
set "MAIN_FILE=%BASE_DIR%\app\main.py"

:: --- Saídas ---
set "BUILD_PATH=%BASE_DIR%\build"
set "DIST_PATH=%BASE_DIR%\dist"
set "OUTPUT_EXE=%BASE_DIR%\%APP_NAME%.exe"

:: ============================================================
:: 🧹 Limpeza inicial
:: ============================================================
echo 🧹 Limpando builds anteriores...
if exist "%BUILD_PATH%" rd /s /q "%BUILD_PATH%"
if exist "%DIST_PATH%" rd /s /q "%DIST_PATH%"
if exist "%OUTPUT_EXE%" del /f /q "%OUTPUT_EXE%"
if exist "%BASE_DIR%\%APP_NAME%.spec" del /f /q "%BASE_DIR%\%APP_NAME%.spec"

:: ============================================================
:: 🧩 Verificações básicas
:: ============================================================
if not exist "%ICON_PATH%" (
    echo ⚠️ AVISO: Ícone não encontrado em "%ICON_PATH%"
    echo    O build continuará com o ícone padrão do Python.
)

if not exist "%MAIN_FILE%" (
    echo ❌ ERRO CRÍTICO: main.py não encontrado em:
    echo    "%MAIN_FILE%"
    echo.
    pause
    exit /b 1
)

:: ============================================================
:: 🏗️ Compilando com PyInstaller
:: ============================================================
echo 🏗️  Gerando executável (Isso pode levar alguns minutos)...

:: Explicação dos comandos:
:: --add-data "ORIGEM;DESTINO": Copia pastas para dentro do executável (na pasta interna 'app')
:: --hidden-import: Força o PyInstaller a incluir bibliotecas que ele as vezes esquece

pyinstaller ^
 --noconfirm ^
 --clean ^
 --onefile ^
 --windowed ^
 --name "%APP_NAME%" ^
 --icon "%ICON_PATH%" ^
 --distpath "%BASE_DIR%" ^
 --workpath "%BUILD_PATH%" ^
 --specpath "%BUILD_PATH%" ^
 --hidden-import "PIL" ^
 --hidden-import "customtkinter" ^
 --hidden-import "pygame" ^
 --add-data "%BASE_DIR%\app\assets;app/assets" ^
 --add-data "%BASE_DIR%\app\screens;app/screens" ^
 --add-data "%BASE_DIR%\app\utils;app/utils" ^
 "%MAIN_FILE%"

:: ============================================================
:: 🧽 Limpeza final
:: ============================================================
echo 🧽 Limpando arquivos temporários...
if exist "%BUILD_PATH%" rd /s /q "%BUILD_PATH%"
if exist "%DIST_PATH%" rd /s /q "%DIST_PATH%"
if exist "%BASE_DIR%\%APP_NAME%.spec" del /f /q "%BASE_DIR%\%APP_NAME%.spec"

:: ============================================================
:: ✅ Resultado final
:: ============================================================
if exist "%OUTPUT_EXE%" (
    echo.
    echo ============================================================
    echo ✅ SUCESSO! Build concluído.
    echo ============================================================
    echo 📁 Executável criado: "%OUTPUT_EXE%"
    echo.
    echo ⚠️ IMPORTANTE:
    echo    As pastas "games" e "system" devem estar AO LADO do .exe
    echo    para que os emuladores funcionem. O .exe não contém elas.
    echo.
    echo ▶️  Pressione qualquer tecla para testar o App...
    pause >nul
    start "" "%OUTPUT_EXE%"
) else (
    echo.
    echo ❌ ERRO: O executável não foi criado. Verifique o log acima.
)

echo.
pause
endlocal