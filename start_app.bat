@echo off
TITLE AI Diet Balance Automatic Launcher
echo ======================================================================
echo 🚀 Starting AI Diet Balance Full-Stack Platform...
echo ======================================================================

set ROOT_DIR=%~dp0
set BACKEND_DIR=%ROOT_DIR%backend
set FRONTEND_DIR=%ROOT_DIR%frontend
set PYTHON_EXE=%BACKEND_DIR%\venv\Scripts\python.exe

echo 🗄️ Running database migrations and seeding admin accounts...
cd /d "%BACKEND_DIR%"
"%PYTHON_EXE%" manage.py migrate --noinput
"%PYTHON_EXE%" seed_db.py

echo ⚡ Launching Django Backend Server (http://localhost:8000)...
start "Django Backend Server (Port 8000)" cmd /k "cd /d "%BACKEND_DIR%" && "%PYTHON_EXE%" manage.py runserver 0.0.0.0:8000"

echo 🎨 Launching React Frontend (http://localhost:5173)...
start "React Frontend Server (Port 5173)" cmd /k "cd /d "%FRONTEND_DIR%" && npm run dev"

timeout /t 3 /nobreak >nul
echo 🌐 Opening Application in Browser: http://localhost:5173
start http://localhost:5173

echo ======================================================================
echo ✅ AI Diet Balance Platform Launched & Running Continuously!
echo ======================================================================
