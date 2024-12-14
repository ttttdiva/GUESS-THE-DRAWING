@REM @echo off

cd /d %~dp0

call venv\Scripts\activate

cd python

python app.py