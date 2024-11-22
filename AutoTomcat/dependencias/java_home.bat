@echo off
setlocal

:: Cambia esta ruta por la ruta de instalación de tu JDK
set "JAVA_HOME_PATH=C:\Program Files\Java\jdk1.8.0_121"

:: Verificar si el directorio existe
if not exist "%JAVA_HOME_PATH%" (
    echo No se encuentra el directorio: %JAVA_HOME_PATH%
    exit /b 1
)

:: Configurar JAVA_HOME
setx JAVA_HOME "%JAVA_HOME_PATH%" /m

:: Añadir %JAVA_HOME%\bin a la variable PATH
set "PATH_TO_ADD=%JAVA_HOME_PATH%\bin"

:: Obtener la variable PATH actual
for /f "skip=2 tokens=2,* delims= " %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do (
    set "OLD_PATH=%%B"
)

:: Añadir el nuevo JAVA_HOME\bin al PATH si no está ya presente
echo %OLD_PATH% | find /i "%PATH_TO_ADD%" >nul
if errorlevel 1 (
    set "NEW_PATH=%OLD_PATH%;%PATH_TO_ADD%"
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%NEW_PATH%" /f
    echo PATH actualizado con: %PATH_TO_ADD%
) else (
    echo PATH ya contiene: %PATH_TO_ADD%
)

endlocal
pause
