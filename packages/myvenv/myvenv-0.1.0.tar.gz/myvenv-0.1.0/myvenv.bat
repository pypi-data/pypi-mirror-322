@echo off
REM ==================================
REM myvenv.bat
REM Create or activate a virtual env
REM in the current CMD shell.
REM ==================================

:: 1) Determine the env name from user or default to "venv".
set "ENV_NAME=venv"
if not "%~1"=="" (
    set "ENV_NAME=%~1"
)

:: 2) If the folder doesn't exist, create the venv.
if not exist "%ENV_NAME%" (
    echo Creating virtual environment "%ENV_NAME%"...
    python -m venv "%ENV_NAME%"
)

:: 3) Update .gitignore if needed
call :UPDATE_GITIGNORE "%ENV_NAME%"

:: 4) Activate in the current CMD shell
echo Activating "%ENV_NAME%"...
call "%ENV_NAME%\Scripts\activate.bat"
goto :EOF

:UPDATE_GITIGNORE
setlocal
set "VENV_NAME=%~1"
set "GITIGNORE=.gitignore"

if not exist "%GITIGNORE%" (
    echo .gitignore not found; creating a new one...
    echo %VENV_NAME%>> "%GITIGNORE%"
    endlocal
    goto :EOF
)

:: Check for existing entry in .gitignore (case-insensitive).
for /f "usebackq tokens=* delims=" %%A in ("%GITIGNORE%") do (
    if /I "%%~A"=="%VENV_NAME%" (
        endlocal
        goto :EOF
    )
)

echo Adding "%VENV_NAME%" to .gitignore...
echo %VENV_NAME%>> "%GITIGNORE%"
endlocal
goto :EOF
