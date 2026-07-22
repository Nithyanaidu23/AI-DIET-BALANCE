param(
    [ValidateSet("Smoke", "Normal", "Stress", "Spike", "Soak")]
    [string]$Scenario = "Smoke",
    [switch]$Headless,
    [int]$WarmupSeconds = 15
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         AI Diet Planner Production Load Test             " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Scenario: $Scenario | Mode: $(if ($Headless) { 'Headless' } else { 'Web UI' })" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# Define Scenario Parameters
$users = 10
$spawnRate = 2
$duration = "1m" # default for smoke test in script
$durationSec = 60
$errThreshold = 1.0  # 1%
$p95Threshold = 500  # 500ms

switch ($Scenario) {
    "Smoke" {
        $users = 10
        $spawnRate = 2
        $duration = "5m"
        $durationSec = 300
        $errThreshold = 0.5
        $p95Threshold = 200
    }
    "Normal" {
        $users = 100
        $spawnRate = 5
        $duration = "20m"
        $durationSec = 1200
        $errThreshold = 1.0
        $p95Threshold = 500
    }
    "Stress" {
        $users = 500
        $spawnRate = 10
        $duration = "1h" # run until fail (or up to 1h)
        $durationSec = 3600
        $errThreshold = 5.0
        $p95Threshold = 1000
    }
    "Spike" {
        $users = 1000
        $spawnRate = 20
        $duration = "10m"
        $durationSec = 600
        $errThreshold = 2.0
        $p95Threshold = 800
    }
    "Soak" {
        $users = 200
        $spawnRate = 5
        $duration = "2h"
        $durationSec = 7200
        $errThreshold = 1.0
        $p95Threshold = 500
    }
}

# 1. Start PostgreSQL Container via Docker Compose
Write-Host "[1/6] Spinning up PostgreSQL database container..." -ForegroundColor Yellow
& docker compose up -d db

# Wait for DB to be healthy
Write-Host "Waiting for database to be healthy..." -ForegroundColor Yellow
$dbHealthy = $false
for ($i = 0; $i -lt 15; $i++) {
    $status = & docker inspect --format='{{json .State.Health.Status}}' diet_planner_db 2>$null
    if ($status -eq '"healthy"') {
        $dbHealthy = $true
        break
    }
    Start-Sleep -Seconds 2
}

if (-not $dbHealthy) {
    Write-Host "Database container is up, continuing..." -ForegroundColor Gray
} else {
    Write-Host "Database is healthy and ready!" -ForegroundColor Green
}

# 2. Update local Python dependencies
Write-Host "[2/6] Syncing Python dependencies..." -ForegroundColor Yellow
& .\backend\venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt

# 3. Run migrations and seed database
Write-Host "[3/6] Running migrations and seeding operational dataset..." -ForegroundColor Yellow
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/diet_planner"
$env:DJANGO_SETTINGS_MODULE = "config.settings.load_test"
& .\backend\venv\Scripts\python.exe .\backend\manage.py migrate
& .\backend\venv\Scripts\python.exe .\backend\manage.py seed_load_test_users --count 1000

# 4. Start local Django development server pointing to PostgreSQL container
Write-Host "[4/6] Starting Django API server locally on port 8001 (load_test settings)..." -ForegroundColor Yellow
$ServerProc = Start-Process -FilePath ".\backend\venv\Scripts\python.exe" `
    -ArgumentList ".\backend\manage.py runserver 8001" `
    -Environment @{ 
        DJANGO_SETTINGS_MODULE = "config.settings.load_test"
        DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/diet_planner"
    } `
    -PassThru -NoNewWindow

Start-Sleep -Seconds 5

if ($ServerProc.HasExited) {
    Write-Error "Failed to start local Django development server."
    exit 1
}

Write-Host "Django server is running (PID: $($ServerProc.Id))." -ForegroundColor Green

# Ensure reports directory exists
New-Item -ItemType Directory -Path ".\backend\reports" -Force | Out-Null

$LocustProc = $null

try {
    # 5. Run Locust
    Write-Host "[5/6] Starting load test runner..." -ForegroundColor Yellow
    if ($Headless) {
        Write-Host "Running Locust in headless mode..." -ForegroundColor Yellow
        Write-Host "Target: $users users (spawn rate $spawnRate/s) for $duration" -ForegroundColor Yellow
        
        # We start locust in background process so we can poll metrics during execution
        $LocustProc = Start-Process -FilePath ".\backend\venv\Scripts\python.exe" `
            -ArgumentList "-m locust -f .\backend\locustfile.py -H http://localhost:8001 --headless -u $users -r $spawnRate --run-time $duration --csv=.\backend\reports\loadtest_$Scenario" `
            -PassThru -NoNewWindow
            
        # 6. Monitor and Collect Metrics
        Write-Host "[6/6] Monitoring performance, server metrics, and database..." -ForegroundColor Yellow
        Write-Host "Warm-up phase of $WarmupSeconds seconds active..." -ForegroundColor DarkYellow
        Start-Sleep -Seconds $WarmupSeconds
        Write-Host "Warm-up phase completed. Active metrics monitoring started." -ForegroundColor Green
        
        $elapsed = $WarmupSeconds
        $violationCounter = 0
        
        while (-not $LocustProc.HasExited -and $elapsed -lt $durationSec) {
            Start-Sleep -Seconds 10
            $elapsed += 10
            
            # Fetch process metrics
            try {
                $process = Get-Process -Id $ServerProc.Id -ErrorAction SilentlyContinue
                if ($process) {
                    $memMb = [math]::Round($process.WorkingSet64 / 1MB, 2)
                    Write-Host "Django Resource Usage: CPU: ~$( [math]::Round(($process.CPU / 10), 1) )% | RAM: $memMb MB" -ForegroundColor DarkGray
                }
            } catch {}
            
            # Query Locust Stats API (Locust hosts a stats endpoint even in headless mode)
            try {
                $stats = Invoke-RestMethod -Uri "http://localhost:8089/stats/requests" -ErrorAction SilentlyContinue
                if ($stats) {
                    $curErrRate = [float]$stats.errors_in_last_10s
                    # Locate the 95th percentile response time for overall requests
                    $curP95 = 0
                    if ($stats.stats) {
                        $totalStat = $stats.stats | Where-Object { $_.name -eq "Total" }
                        if ($totalStat) {
                            $curP95 = $totalStat.ninetyninth_response_time # fallback to 99th or 95th if available
                        }
                    }
                    
                    Write-Host "Locust Stats: Errors/10s: $curErrRate | Total RPS: $($stats.total_rps) | State: $($stats.state)" -ForegroundColor DarkCyan
                    
                    # Check Stress Test Degradation Condition
                    if ($Scenario -eq "Stress") {
                        if ($curErrRate -gt $errThreshold -or $curP95 -gt $p95Threshold) {
                            $violationCounter += 10
                            Write-Host "WARNING: Degradation threshold breached (Error Rate: $curErrRate%, p95: $curP95 ms) for $violationCounter seconds." -ForegroundColor Red
                            if ($violationCounter -ge 180) { # 3 minutes (180s) of sustained degradation
                                Write-Host "CRITICAL: Sustained degradation for 3 minutes. Stopping stress test." -ForegroundColor Red
                                break
                            }
                        } else {
                            $violationCounter = [math]::Max(0, $violationCounter - 10)
                        }
                    }
                }
            } catch {}
        }
        
        if (-not $LocustProc.HasExited) {
            Write-Host "Stopping Locust load test process..." -ForegroundColor Yellow
            Stop-Process -Id $LocustProc.Id -Force
        }
        
    } else {
        Write-Host "Starting Locust Web UI..." -ForegroundColor Yellow
        Write-Host "Open http://localhost:8089 in your browser to run the tests." -ForegroundColor Green
        Write-Host "Press CTRL+C in this terminal to shut down the load test and stop the Django API server." -ForegroundColor Yellow
        & .\backend\venv\Scripts\python.exe -m locust -f .\backend\locustfile.py -H http://localhost:8001
    }
}
finally {
    # Clean up processes
    if ($LocustProc -and -not $LocustProc.HasExited) {
        Stop-Process -Id $LocustProc.Id -Force
    }
    if ($ServerProc -and -not $ServerProc.HasExited) {
        Write-Host "Stopping Django API server..." -ForegroundColor Yellow
        Stop-Process -Id $ServerProc.Id -Force
        Write-Host "Django API server stopped." -ForegroundColor Green
    }
    
    # 7. Collect PostgreSQL Database Diagnostics
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "       PostgreSQL Database Performance Diagnostics        " -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    
    # Cache hit ratio
    $cacheQuery = "SELECT round(sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read) + 1.0) * 100.0, 2) AS cache_hit_ratio FROM pg_statio_user_tables;"
    Write-Host "1. Database Cache Hit Ratio:" -ForegroundColor Yellow
    & docker compose exec -T db psql -U postgres -d diet_planner -c $cacheQuery
    
    # Seq Scans vs Index Scans
    $scanQuery = "SELECT sum(seq_scan) AS seq_scans, sum(idx_scan) AS idx_scans FROM pg_stat_user_tables;"
    Write-Host "2. Table Sequential Scans vs Index Scans:" -ForegroundColor Yellow
    & docker compose exec -T db psql -U postgres -d diet_planner -c $scanQuery
    
    # Connection counts
    $connQuery = "SELECT count(*) AS total_connections, count(nullif(state, 'idle')) AS active_connections FROM pg_stat_activity;"
    Write-Host "3. Current Database Connections:" -ForegroundColor Yellow
    & docker compose exec -T db psql -U postgres -d diet_planner -c $connQuery
    
    # Waiting Locks
    $lockQuery = "SELECT count(*) AS blocked_queries_waiting_locks FROM pg_locks WHERE granted = false;"
    Write-Host "4. Locked Queries Waiting for Resources:" -ForegroundColor Yellow
    & docker compose exec -T db psql -U postgres -d diet_planner -c $lockQuery
    
    # Slow Queries
    $slowQuery = "SELECT pid, age(clock_timestamp(), query_start) AS duration, query FROM pg_stat_activity WHERE state != 'idle' AND age(clock_timestamp(), query_start) > interval '1 second' ORDER BY duration DESC LIMIT 5;"
    Write-Host "5. Running queries longer than 1 second:" -ForegroundColor Yellow
    & docker compose exec -T db psql -U postgres -d diet_planner -c $slowQuery
    
    Write-Host "Load test execution completed!" -ForegroundColor Green
}
