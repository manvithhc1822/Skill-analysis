@echo off
title Skill Gap Analyzer

cd /d "%~dp0"

echo Starting Skill Gap Analyzer...

start "Skill Gap Analyzer Server" /min cmd /c "python server.py"

timeout /t 1 /nobreak >nul

start "" "http://127.0.0.1:5001"

exit