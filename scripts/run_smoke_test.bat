@echo off
set BASE_URL=http://127.0.0.1:8000

REM Try local venv python first if present
if exist "%~dp0..\..\myenv\Scripts\python.exe" (
  set PYEXE=%~dp0..\..\myenv\Scripts\python.exe
) else (
  set PYEXE=python
)

echo Running smoke test against %BASE_URL%
"%PYEXE%" "%~dp0smoke_test.py"
if %errorlevel% neq 0 (
  echo Smoke test failed. Ensure the server is running: python Downloads/inkle/manage.py runserver
  pause
  exit /b 1
)

echo Smoke test completed successfully.
pause
