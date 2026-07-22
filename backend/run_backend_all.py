"""
Master Backend Execution Script — AI Diet Balance Platform
Runs database migrations, seeds admin accounts, loads food database,
executes tests, and starts the Django backend server.
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run_cmd(args, description):
    print(f"\n==================================================")
    print(f"⚙️  {description}")
    print(f"==================================================")
    result = subprocess.run(args, cwd=BASE_DIR)
    if result.returncode != 0:
        print(f"⚠️ Warning: Command exited with code {result.returncode}")
    else:
        print(f"✅ {description} completed successfully.")

def main():
    python_exe = sys.executable

    print("\n🚀 Starting Full Backend Initialization & Execution...")

    # 1. Django System Checks
    run_cmd([python_exe, "manage.py", "check"], "Running Django System Check")

    # 2. Make Migrations
    run_cmd([python_exe, "manage.py", "makemigrations"], "Creating Database Migrations")

    # 3. Apply Migrations
    run_cmd([python_exe, "manage.py", "migrate", "--noinput"], "Applying Database Migrations")

    # 4. Seed Administrator Accounts
    run_cmd([python_exe, "seed_db.py"], "Seeding Administrator Credentials")

    # 5. Load Food Database Items
    run_cmd([python_exe, "manage.py", "load_foods"], "Loading Nutrition Food Database")

    # 6. Execute Test Suite
    run_cmd([python_exe, "manage.py", "test"], "Executing Backend Test Suite")

    # 7. Start Django Server
    print("\n==================================================")
    print("⚡ Starting Django Backend Server on http://localhost:8000")
    print("==================================================")
    subprocess.run([python_exe, "manage.py", "runserver", "0.0.0.0:8000"], cwd=BASE_DIR)

if __name__ == "__main__":
    main()
