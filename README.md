<div align="center">

# 🥗 AI Diet Balance

### Enterprise AI-Powered Nutrition & Health SaaS Platform

*Generate personalized 7-day meal plans in seconds — powered by Google Gemini AI*

[![Build Status](https://github.com/Nithyanaidu23/AI-DIET-BALANCE/actions/workflows/ci.yml/badge.svg)](https://github.com/Nithyanaidu23/AI-DIET-BALANCE/actions)
[![Python](https://img.shields.io/badge/Python-3.12-3776ab.svg?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.1-092e20.svg?logo=django)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18-61dafb.svg?logo=react)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ed.svg?logo=docker)](https://docker.com)
[![Gemini AI](https://img.shields.io/badge/Google-Gemini%201.5-8e44ad.svg?logo=google)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Nithyanaidu23/AI-DIET-BALANCE)](https://github.com/Nithyanaidu23/AI-DIET-BALANCE/commits/main)
[![Issues](https://img.shields.io/github/issues/Nithyanaidu23/AI-DIET-BALANCE)](https://github.com/Nithyanaidu23/AI-DIET-BALANCE/issues)

</div>

---

## 🌐 Live Demo

| Environment | URL | Status |
|---|---|---|
| 🌍 **Live Web App** | **[https://impending-lagoon-mustard.ngrok-free.dev](https://impending-lagoon-mustard.ngrok-free.dev)** | 🟢 Online |
| 🐙 **GitHub Pages** | **[https://Nithyanaidu23.github.io/AI-DIET-BALANCE/](https://Nithyanaidu23.github.io/AI-DIET-BALANCE/)** | 🟢 Online |
| 💻 **Local App** | `http://localhost:5173` | 🔵 Local Dev |
| ⚡ **Local API** | `http://localhost:8000/api/` | 🔵 Local Dev |
| 📄 **Swagger UI** | `http://localhost:8000/api/schema/swagger-ui/` | 🔵 Local Dev |
| 👑 **Admin Console** | `http://localhost:8000/admin/` | 🔵 Local Dev |

---

## 📖 3. Project Overview

### What is AI Diet Balance?

**AI Diet Balance** is a full-stack, production-grade, multi-tenant **SaaS platform** that uses Google Gemini AI to generate personalized 7-day meal plans based on an individual's health profile, dietary goals, and nutritional science (Mifflin-St Jeor BMR, TDEE, body fat estimation, and ideal weight formulas).

### Why was it built?

Traditional diet plans are expensive, generic, and rarely sustainable. Most apps are either too simple (basic calorie counters) or too complicated (requiring a nutritionist). AI Diet Balance fills the gap with an intelligent, automated system that delivers **personalized, science-backed nutrition plans instantly and for free**.

### Who is it for?
- 🏋️ Athletes and fitness enthusiasts
- 🏥 Healthcare professionals and dietitians
- 💼 Individuals managing chronic conditions
- 🏢 Wellness startups and SaaS companies

### Problem → Solution

| Problem | Our Solution |
|---|---|
| Expensive nutritionist consultations | AI-generated personalized meal plans in seconds |
| Generic diet apps | Profiles built from age, weight, height, activity level, and goals |
| No grocery planning | Auto-generated shopping lists from meal plans |
| Inconsistent tracking | Real-time water, BMI, and macro dashboards |
| No admin visibility | Full multi-tenant admin dashboard with analytics |

---

## ✨ 4. Features

<table>
<tr>
<td>

### 🤖 AI & Nutrition
- ✅ AI Meal Planner (Gemini 1.5)
- ✅ Personalized 7-Day Diet Plans
- ✅ Food Database (1,000+ items)
- ✅ Macro Nutrient Tracking
- ✅ BMI & BMR Calculator
- ✅ TDEE & Body Fat Estimator
- ✅ Water Intake Tracker
- ✅ Grocery List Generator

</td>
<td>

### 📊 Analytics & Reports
- ✅ Nutrition Dashboard
- ✅ KPI Cards & Progress Charts
- ✅ Weekly Progress Visualizations
- ✅ AI Recommendations
- ✅ Export CSV / Excel / JSON
- ✅ Admin Analytics Console
- ✅ Platform-wide Usage Reports
- ✅ AI Request & Log Audit Trail

</td>
<td>

### 🔐 Platform & Security
- ✅ JWT Authentication
- ✅ Role-Based Access (Admin/User)
- ✅ Multi-Tenant Admin Dashboard
- ✅ Rate Limiting & DDoS Protection
- ✅ REST API (60+ endpoints)
- ✅ Swagger / OpenAPI 3.0 Docs
- ✅ GitHub Actions CI/CD
- ✅ Docker Compose Deployment

</td>
</tr>
</table>

---

## 🖼️ 5. Screenshots

| Login Page | User Dashboard | AI Meal Planner |
|---|---|---|
| Mobile-first auth screen with animated layout | KPI cards, macro charts, water tracker summary | 7-day plan generator with nutrient targets |

| Admin Panel | Analytics | Mobile View |
|---|---|---|
| User management, AI audit logs, system health | Recharts bar & line graphs for platform metrics | Full responsive drawer navigation on 320px+ |

> 📸 **Live demo accessible at** [https://impending-lagoon-mustard.ngrok-free.dev](https://impending-lagoon-mustard.ngrok-free.dev)

---

## 🏗️ 6. Architecture Diagram

```text
                    👤 User (Any Device / Screen Size)
                              │
                    ┌─────────▼──────────┐
                    │   React 18 + Vite  │  ← Mobile-First Responsive
                    │   Tailwind CSS     │    Sidebar Drawer, Sticky Nav
                    │   TanStack Query   │    Recharts Dashboards
                    └─────────┬──────────┘
                              │  HTTP REST (JWT Bearer Token)
                    ┌─────────▼──────────┐
                    │  Django REST API   │  ← DRF, SimpleJWT, Throttling
                    │  60+ Endpoints     │    CorsHeaders, drf-spectacular
                    │  Rate Limiting     │    OpenAPI 3.0 / Swagger UI
                    └──────┬─────┬───────┘
                           │     │
          ┌────────────────▼──┐  └──────▼─────────────────┐
          │   PostgreSQL DB   │       │  Google Gemini AI  │
          │  15+ Tables       │       │  1.5 Flash Model   │
          │  15,000+ Records  │       │  Zero-Downtime     │
          └────────┬──────────┘       │  Fallback Client   │
                   │                  └────────────────────┘
     ┌─────────────┴──────────────┐
     │                            │
     ▼                            ▼
┌──────────────┐         ┌────────────────────┐
│ Thread-Safe  │         │  Automated ETL     │
│ Multi-Export │         │  Pipeline (Pandas) │
│ CSV/JSON/XLS │         │  Analytics Engine  │
└──────────────┘         └────────────────────┘
```

---

## 🛠️ 7. Tech Stack

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| **React** | 18 | UI Component Framework |
| **Vite** | 5 | Build Tool & Dev Server |
| **Tailwind CSS** | 3 | Utility-First Styling |
| **TanStack Query** | 5 | Server State Management |
| **Recharts** | 2 | Data Visualization Charts |
| **React Hook Form** | 7 | Form State Management |
| **Zod** | 3 | Schema Validation |
| **Lucide Icons** | Latest | Icon System |

### Backend
| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.12 | Core Language |
| **Django** | 5.1 | Web Framework |
| **Django REST Framework** | 3.15 | REST API Layer |
| **SimpleJWT** | 5 | JWT Authentication |
| **drf-spectacular** | 0.27 | OpenAPI 3.0 Docs |
| **Pandas** | 2.2 | ETL & Analytics |
| **OpenPyXL** | 3.1 | Excel Export |
| **Gunicorn** | 22 | Production WSGI Server |

### Database & DevOps
| Technology | Purpose |
|---|---|
| **PostgreSQL 16** | Production Relational Database |
| **SQLite** | Local Development Database |
| **Docker & Compose** | Containerization & Orchestration |
| **GitHub Actions** | CI/CD Automation Pipeline |
| **Locust** | API Performance Load Testing |
| **Google Gemini 1.5** | AI Meal Plan Generation |

---

## 📂 8. Folder Structure

```
AI-DIET-BALANCE/
│
├── 📁 backend/                     # Django REST Framework Backend
│   ├── 📁 accounts/                # User Authentication & RBAC
│   │   ├── management/commands/    # create_admin_accounts seeder
│   │   └── migrations/             # Database Migrations
│   ├── 📁 ai_engine/               # Google Gemini AI Client + Fallback
│   ├── 📁 activity_logs/           # User Activity & Audit Trail
│   ├── 📁 health/                  # System Health Monitoring APIs
│   ├── 📁 mealplanner/             # Meal Plan CRUD + AI Generation
│   ├── 📁 nutrition/               # Food Database & Nutrition API
│   ├── 📁 users/                   # User Profile & Settings
│   ├── 📁 config/                  # Django Settings & URL Configuration
│   ├── 📁 exports/                 # Auto-generated CSV, JSON, Excel
│   ├── 📄 locustfile.py            # Load Testing Suite
│   ├── 📄 manage.py                # Django Management Entry Point
│   └── 📄 requirements.txt         # Python Dependencies
│
├── 📁 frontend/                    # React 18 + Vite Frontend
│   ├── 📁 src/
│   │   ├── 📁 components/          # Reusable React Components
│   │   │   ├── Sidebar.jsx         # Mobile-First Drawer Navigation
│   │   │   ├── AdminSidebar.jsx    # Admin Drawer Navigation
│   │   │   ├── Navbar.jsx          # Sticky Top Bar + Hamburger Toggle
│   │   │   ├── AppLayout.jsx       # User App Layout Manager
│   │   │   └── AdminLayout.jsx     # Admin Layout Manager
│   │   ├── 📁 pages/               # Page-Level React Views
│   │   │   ├── Dashboard.jsx       # Main User Dashboard
│   │   │   ├── MealPlanner.jsx     # AI Meal Plan Generator
│   │   │   ├── BMICalculator.jsx   # BMI, BMR, TDEE Calculator
│   │   │   ├── FoodSearch.jsx      # Food Database Browser
│   │   │   ├── Profile.jsx         # User Profile Editor
│   │   │   ├── History.jsx         # Meal Plan History
│   │   │   ├── Landing.jsx         # Public Landing Page
│   │   │   ├── Login.jsx           # Authentication
│   │   │   ├── Register.jsx        # Registration
│   │   │   ├── 📁 admin/           # Admin-Only Pages
│   │   │   └── 📁 user/            # User-Specific Pages
│   │   ├── 📁 context/             # React Context (Auth, Theme)
│   │   ├── 📁 services/            # Axios API Service Layer
│   │   ├── 📁 hooks/               # Custom React Hooks
│   │   └── 📄 index.css            # Global Design System (Tailwind)
│   ├── 📄 vite.config.js           # Vite Build Configuration
│   ├── 📄 tailwind.config.js       # Tailwind CSS Design Tokens
│   └── 📄 package.json             # Node Dependencies
│
├── 📄 docker-compose.yml           # Full-Stack Docker Orchestration
├── 📄 run_load_tests.ps1           # Locust Load Test Launcher Script
├── 📄 performance_dashboard.md     # Performance Benchmarks & Results
└── 📄 README.md                    # This File
```

---

## ⚙️ 9. Installation Guide

### Prerequisites
- Python `3.12+`
- Node.js `20+`
- Git

### Step-by-Step Setup

```powershell
# 1. Clone the Repository
git clone https://github.com/Nithyanaidu23/AI-DIET-BALANCE.git
cd AI-DIET-BALANCE

# 2. Backend: Create Virtual Environment
cd backend
python -m venv venv
.\venv\Scripts\activate     # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install Python Dependencies
pip install -r requirements.txt

# 4. Configure Environment Variables (create .env file)
copy .env.example .env

# 5. Run Database Migrations
python manage.py migrate

# 6. Seed Administrator Accounts
python manage.py create_admin_accounts

# 7. Start Backend Server
python manage.py runserver
# Backend runs at: http://localhost:8000

# 8. Frontend: Install Dependencies (new terminal)
cd ../frontend
npm install

# 9. Start Frontend Dev Server
npm run dev
# Frontend runs at: http://localhost:5173
```

---

## 🐳 10. Docker Setup

```bash
# Build and launch all services (Backend, Frontend, PostgreSQL)
docker-compose up --build

# Run in background (detached mode)
docker-compose up --build -d

# Stop all services
docker-compose down

# Run migrations inside Docker
docker-compose exec backend python manage.py migrate
```

After launch:
- **Frontend App** → http://localhost:5173
- **Backend API** → http://localhost:8000/api/
- **Swagger Docs** → http://localhost:8000/api/schema/swagger-ui/
- **PostgreSQL DB** → localhost:5432

---

## 🔑 11. Environment Variables

Create a `.env` file inside the `backend/` folder:

```env
# Django Core
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/aidiet
# Leave empty to use SQLite for local development

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here

# JWT Auth
JWT_SECRET=your-jwt-secret-key-here

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

> **Note**: If `GEMINI_API_KEY` is missing, the AI engine automatically falls back to a built-in deterministic 7-day meal plan so the app never crashes.

---

## 📡 12. API Documentation

### Interactive Docs
| Format | URL |
|---|---|
| 🔵 **Swagger UI** | `http://localhost:8000/api/schema/swagger-ui/` |
| 📚 **ReDoc** | `http://localhost:8000/api/schema/redoc/` |
| 📄 **OpenAPI JSON** | `http://localhost:8000/api/schema/` |
| 🏥 **Health Check** | `http://localhost:8000/api/health/status/` |

### Key API Endpoints
```
POST   /api/accounts/login/          → JWT Login
POST   /api/accounts/register/       → User Registration
POST   /api/accounts/token/refresh/  → JWT Refresh

GET    /api/mealplanner/plans/       → List All Meal Plans
POST   /api/mealplanner/generate/    → Generate AI Meal Plan
GET    /api/mealplanner/grocery/     → Get Grocery List

GET    /api/nutrition/foods/         → Search Food Database
GET    /api/health/bmi/              → Get BMI Records
POST   /api/health/water/            → Log Water Intake

GET    /api/admin/users/             → Admin: List All Users
GET    /api/admin/analytics/         → Admin: Platform Analytics
GET    /api/admin/ai-logs/           → Admin: AI Request Audit
```

---

## 🗄️ 13. Database Schema

```text
┌──────────────┐   ┌───────────────┐   ┌────────────────┐
│    Users     │──▶│   Profiles    │──▶│  Subscriptions │
│  (accounts)  │   │ (health data) │   │ (Free/Pro/Ent) │
└──────────────┘   └───────────────┘   └────────────────┘
       │
       ├──▶ ┌───────────────┐   ┌────────────────┐
       │    │  Meal Plans   │──▶│  Meal Days     │
       │    │  (7-day AI)   │   │  (daily meals) │
       │    └───────────────┘   └────────────────┘
       │
       ├──▶ ┌───────────────┐   ┌────────────────┐
       │    │  Food Items   │   │   BMI Records  │
       │    │ (1,000+ items)│   │  (historical)  │
       │    └───────────────┘   └────────────────┘
       │
       ├──▶ ┌───────────────┐   ┌────────────────┐
       │    │  Water Logs   │   │ Activity Logs  │
       │    │  (daily ml)   │   │  (audit trail) │
       │    └───────────────┘   └────────────────┘
       │
       └──▶ ┌───────────────┐   ┌────────────────┐
            │    Events     │   │    Payments    │
            │  (telemetry)  │   │ (SaaS billing) │
            └───────────────┘   └────────────────┘
```

---

## 🤖 14. AI Workflow

```text
  👤 User fills Health Profile
  (age, weight, height, activity, dietary goal)
           │
           ▼
  📋 System calculates:
  BMR → TDEE → Target Calories → Macro Split
           │
           ▼
  🤖 Google Gemini 1.5 Flash
  Receives structured JSON prompt:
  {goal, calories, protein, carbs, fat, preferences}
           │
           ├──── ✅ API Success → Parse & Validate JSON Response
           │
           └──── ⚠️ API Failure → Deterministic Fallback Meal Plan
                   (Zero downtime — app never breaks)
           │
           ▼
  📦 Meal Plan Stored in PostgreSQL
  (7 days × 3 meals × full nutrition data)
           │
           ▼
  📊 User Dashboard Updates:
  Macro Charts, Grocery List, PDF Export
```

---

## 📊 15. Dashboard Features

### User Dashboard
- **KPI Cards**: Calorie target, protein/carb/fat macros, water intake percentage, BMI status
- **Macro Pie Chart**: Real-time donut chart showing protein/carb/fat distribution
- **Weekly Progress Bar**: Daily calorie tracking against TDEE goals
- **Water Tracker**: Animated progress bar with quick-add buttons (250ml, 500ml, 750ml)
- **AI Recommendations**: Personalized tips from Gemini AI

### Admin Dashboard
- **Platform KPIs**: Total users, active meal plans, AI requests count, system health
- **User Registration Velocity**: Bar chart of daily sign-ups
- **AI Audit Log**: Full prompt history, IP addresses, token estimates, success/fail status
- **System Monitoring**: CPU, memory, database, and Gemini API health in real-time

---

## 🔐 16. Security

| Security Layer | Implementation |
|---|---|
| **JWT Authentication** | SimpleJWT with access + refresh token rotation |
| **Password Hashing** | Django PBKDF2 with SHA-256 (100,000 iterations) |
| **Role-Based Access** | `IsAdminRole` custom permission class on all admin endpoints |
| **Rate Limiting** | Differentiated throttling per user type and endpoint |
| **Input Validation** | Zod (frontend) + DRF serializer validation (backend) |
| **CORS Protection** | `django-cors-headers` with whitelisted origins |
| **Audit Logging** | Complete request lifecycle logs in `ActivityLog` model |
| **SQL Injection** | Django ORM parameterized queries — no raw SQL |

### Rate Limits
```
Anonymous Users   → 100 requests/day
Authenticated     → 1,000 requests/day
Auth Endpoints    → 10 requests/minute
AI Generation     → 30 requests/hour
```

---

## ⚡ 17. Performance

| Optimization | Details |
|---|---|
| **Database Indexes** | Indexed on `user`, `created_at`, `email`, `category` columns |
| **Query Optimization** | `select_related()` / `prefetch_related()` on all list endpoints |
| **Thread-Safe Exports** | `threading.Lock()` on CSV/JSON/Excel write operations |
| **Zero-Downtime AI** | Deterministic fallback client if Gemini API is unavailable |
| **Docker Deployment** | Gunicorn WSGI with multi-worker process configuration |
| **Load Testing** | Locust 2.29 with 35,000+ seeded user records for benchmarking |

---

## 🧪 18. Testing

```powershell
# Run all Django unit tests
.\venv\Scripts\python.exe manage.py test

# Run with verbosity
.\venv\Scripts\python.exe manage.py test --verbosity=2

# Run Locust load test (Interactive Web UI)
.\run_load_tests.ps1 -Scenario Smoke

# Run Locust load test (Headless, 20 min)
.\run_load_tests.ps1 -Scenario Normal -Headless
```

### Test Coverage
| Type | Count | Coverage |
|---|---|---|
| Unit Tests | 38 tests | Models, Serializers, Permissions |
| API Tests | Included | All REST endpoints validated |
| Load Tests | 6 Scenarios | Smoke, Normal, Spike, Stress, Soak, Endurance |

---

## 🔄 19. CI/CD Pipeline

```text
  📝 Developer commits code
           │
           ▼
  🐙 Git Push → GitHub Repository
           │
           ▼
  ⚙️ GitHub Actions Triggered (.github/workflows/ci.yml)
           │
           ├──▶ 🐍 Setup Python 3.12 environment
           │
           ├──▶ 📦 pip install -r requirements.txt
           │
           ├──▶ 🗄️  python manage.py migrate
           │
           ├──▶ 🧪 python manage.py test (38 unit tests)
           │
           ├──▶ 🔥 Locust Smoke Load Test (60 seconds, 10 users)
           │
           └──▶ ✅ Build Complete — All checks passed
```

---

## 📈 20. Performance Results

| Scenario | Users | Duration | Avg Response | Throughput | Error Rate |
|---|---|---|---|---|---|
| **Smoke Test** | 10 | 60s | < 200ms | ~50 req/s | 0% |
| **Normal Load** | 100 | 5 min | < 350ms | ~200 req/s | < 1% |
| **Spike Test** | 500 | 10 min | < 800ms | ~400 req/s | < 3% |
| **Stress Test** | 1,000 | 20 min | < 1.2s | ~600 req/s | < 5% |

> 📊 Full benchmark details in [performance_dashboard.md](./performance_dashboard.md)

---

## 🛣️ 21. Roadmap

- [ ] 📱 **Native Mobile App** — React Native iOS & Android
- [ ] 💬 **AI Chatbot** — Real-time Gemini nutrition assistant
- [ ] ⌚ **Wearable Integration** — Fitbit, Apple Watch, Google Fit sync
- [ ] 🌍 **Multi-Language Support** — i18n / l10n for global users
- [ ] 🔔 **Push Notifications** — Meal reminders & hydration alerts
- [ ] 💳 **Stripe Payments** — Pro & Enterprise subscription billing
- [ ] 📊 **Advanced Analytics** — ML-powered nutrition trend predictions
- [ ] 🏥 **Healthcare API** — FHIR / HL7 EHR integration

---

## 🤝 22. Contributing

We welcome contributions from the community!

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/AI-DIET-BALANCE.git

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes and commit
git commit -m "feat: add your feature description"

# 5. Push to your fork
git push origin feature/your-feature-name

# 6. Open a Pull Request on GitHub
```

### Contribution Guidelines
- Follow existing code style and conventions
- Write meaningful commit messages (`feat:`, `fix:`, `docs:`, `refactor:`)
- Add unit tests for new features
- Update documentation if needed

---

## 📄 23. License

```
MIT License

Copyright (c) 2025 AI Diet Balance Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

---

## 👨‍💻 24. Authors

<table>
<tr>
<td align="center">
<strong>Nithya Serala</strong><br/>
Lead Developer & AI Engineer<br/>
<a href="https://github.com/Nithyanaidu23">GitHub</a> •
<a href="mailto:nithyaserala545@gmail.com">Email</a>
</td>
<td align="center">
<strong>Ganesh Polaiah Mallam</strong><br/>
Full-Stack Developer & DevOps<br/>
<a href="mailto:polaiahmallam8@gmail.com">Email</a>
</td>
</tr>
</table>

---

## ⚡ Quick Copy-Paste Commands

```powershell
# Push all updates to GitHub
cd c:\Users\polai\OneDrive\Desktop\aiwebsite; git add .; git commit -m "feat: update"; git push origin main --force

# Start Backend
cd backend; .\venv\Scripts\python.exe manage.py runserver

# Start Frontend
cd frontend; npm run dev -- --host 0.0.0.0

# Docker Full Stack
docker-compose up --build
```

---

<div align="center">

**⭐ If you find this project useful, please give it a star on GitHub! ⭐**

[![GitHub Stars](https://img.shields.io/github/stars/Nithyanaidu23/AI-DIET-BALANCE?style=social)](https://github.com/Nithyanaidu23/AI-DIET-BALANCE)

*Built with ❤️ using React 18, Django 5, and Google Gemini AI*

</div>
