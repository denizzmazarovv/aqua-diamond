@echo off
REM Push AQUADIAMOND site to GitHub. Usage: double-click, or: push.bat "commit message"
cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
  echo [!] Git is not installed. Download: https://git-scm.com/download/win
  pause
  exit /b 1
)

git config user.name >nul 2>nul
if errorlevel 1 (
  set /p GNAME=Your name for commits: 
  set /p GMAIL=Your email for commits: 
  call git config --global user.name "%%GNAME%%"
  call git config --global user.email "%%GMAIL%%"
)

if not exist ".git" (
  git init
  git remote add origin https://github.com/denizzmazarovv/aqua-diamond.git
)
git branch -M main

git add -A
set "MSG=%~1"
if "%MSG%"=="" set "MSG=Update site %date% %time:~0,5%"
git commit -m "%MSG%"

git pull --rebase origin main 2>nul
git push -u origin main
if errorlevel 1 (
  echo.
  echo [!] Push failed. Check your internet and GitHub login.
) else (
  echo.
  echo [OK] Done: https://github.com/denizzmazarovv/aqua-diamond
)
pause
