# ==============================================================================
# AI Diet Balance - Automatic Continuous Full Stack Launcher Script (Windows)
# Seeds DB, launches Django Backend & React Frontend continuously, opens Browser
# ==============================================================================

Write-Host "Starting AI Diet Balance Platform..." -ForegroundColor Cyan

$ROOT_DIR = $PSScriptRoot
$BACKEND_DIR = Join-Path $ROOT_DIR "backend"
$FRONTEND_DIR = Join-Path $ROOT_DIR "frontend"
$PYTHON_EXE = Join-Path $BACKEND_DIR "venv\Scripts\python.exe"

# 1. Database Migrations & Seeding Admin Accounts
Write-Host "Running database migrations and seeding admin accounts..." -ForegroundColor Green
Set-Location $BACKEND_DIR
& $PYTHON_EXE manage.py migrate --noinput
& $PYTHON_EXE seed_db.py

# 2. Launch Django Backend Server in dedicated persistent window
Write-Host "Launching Django Backend Server on http://localhost:8000 ..." -ForegroundColor Cyan
Start-Process "cmd.exe" -ArgumentList "/k cd /d `"$BACKEND_DIR`" && `"$PYTHON_EXE`" manage.py runserver 0.0.0.0:8000"

# 3. Launch React Frontend Server in dedicated persistent window
Write-Host "Launching React Frontend on http://localhost:5173 ..." -ForegroundColor Cyan
Start-Process "cmd.exe" -ArgumentList "/k cd /d `"$FRONTEND_DIR`" && npm run dev"

# 4. Wait 3 seconds and open Browser
Start-Sleep -Seconds 3
Write-Host "Opening Application in Browser: http://localhost:5173" -ForegroundColor Green
Start-Process "http://localhost:5173"

Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host "AI Diet Balance is RUNNING CONTINUOUSLY!" -ForegroundColor Green
Write-Host "  - Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  - Backend API: http://localhost:8000/api/" -ForegroundColor White
Write-Host "  - Swagger UI: http://localhost:8000/api/schema/swagger-ui/" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Yellow
