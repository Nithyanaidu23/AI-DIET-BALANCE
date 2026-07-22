# 🥗 AI Diet Planner — Production-Grade SaaS Architecture

A **production-grade, multi-tenant AI Diet Planner SaaS platform** built with modern software architecture principles: Django REST Framework, PostgreSQL, React 18 + Vite, automated event collection, thread-safe multi-format data exports (CSV, JSON, Excel), automated ETL data pipeline, rate limiting, and CI/CD automation.

---

## 📐 1. Architecture Diagram

```text
               ┌─────────────────────────────────────────────────────────┐
               │              React 18 + Vite Frontend Client            │
               │   (TanStack Query, Tailwind CSS, Recharts, jsPDF)       │
               └────────────────────────────┬────────────────────────────┘
                                            │ HTTP / REST API (JWT)
                                            ▼
               ┌─────────────────────────────────────────────────────────┐
               │           Django REST Framework API Gateway             │
               │  (SimpleJWT, CorsHeaders, DRF Throttling, DRF Spectacular)│
               └──────────────┬──────────────────────────┬───────────────┘
                              │                          │
              ┌───────────────▼───────────┐    ┌─────────▼─────────────┐
              │    SQLite / PostgreSQL    │    │   Google Gemini API   │
              │  (15+ Normalized Tables)  │    │ (Meal Plan Generation)│
              └───────────────┬───────────┘    └───────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
┌───────────────────────────┐           ┌────────────────────────────┐
│   Thread-Safe Exporter    │           │    Automated ETL Engine    │
│  (CSV, JSON, Excel .xlsx) │           │    (Pandas Aggregations)   │
└───────────────────────────┘           └────────────────────────────┘
```

---

## 🗄️ 2. Database Entity Relationship (ER) Schema

```text
[User] (1) ─────── (1) [UserProfile]
  │
  ├─ (1) ─────── (1) [Subscription] (1) ─────── (*) [Payment]
  │
  ├─ (1) ─────── (*) [MealPlan] (1) ─────── (*) [Meal]
  │                     │
  │                     └─ (1) ─────── (*) [GroceryItem]
  │
  ├─ (1) ─────── (*) [FavoriteMeal]
  ├─ (1) ─────── (*) [BMIRecord]
  ├─ (1) ─────── (*) [WaterTracker]
  ├─ (1) ─────── (*) [ExerciseLog]
  ├─ (1) ─────── (*) [Notification]
  ├─ (1) ─────── (*) [Feedback]
  ├─ (1) ─────── (*) [LoginHistory]
  ├─ (1) ─────── (*) [ActivityLog]
  └─ (1) ─────── (*) [AnalyticsEvent]
```

---

## ✨ 3. Key Features

- 🔐 **Authentication & RBAC**: Email-based JWT login, refresh token rotation, Admin vs. User roles (`IsAdminRole`).
- 🤖 **Deterministic AI Diet Engine**: Combines Mifflin-St Jeor & TDEE formulas with Google Gemini AI for zero-hallucination diet plans.
- 💳 **SaaS Monetization & Tiers**: Track `Subscription` (Free, Pro, Enterprise) and `Payment` histories.
- 📊 **Auto Data Collection Pipeline**: Stream user interactions to the `events` table with telemetry metrics (latency, token estimates, costs).
- 📁 **Multi-Format Auto Exporter**: Thread-safe automatic generation of `.csv`, `.json`, and `.xlsx` Excel files across all 15+ models.
- 🔄 **Automated ETL Pipeline**: Extract, transform, and aggregate data metrics into warehouse analytics summaries using Pandas.
- ⏱️ **Differentiated Rate Limiting**: Protect endpoints against DDoS (`anon`: 100/day, `user`: 1000/day, `auth`: 10/min, `ai`: 30/hour).
- 🏥 **Health & System Monitoring API**: Live health endpoint `/api/health/status/` returning database connectivity and metrics.
- 🧪 **Test Suite**: 38 unit tests covering calculations, authentication, serializers, export engines, and endpoints.
- 🐳 **Docker & CI/CD**: Multi-container Docker Compose setup and GitHub Actions workflow.

---

## 🛠️ 4. Tech Stack & Dependencies

| Layer | Technology |
|---|---|
| **Frontend** | React 18, Vite 5, Tailwind CSS 3, Recharts, TanStack Query |
| **Backend Framework** | Python 3.12, Django 5.1, Django REST Framework 3.15 |
| **Auth & Security** | djangorestframework-simplejwt, django-cors-headers, python-decouple |
| **AI Integration** | Google Generative AI SDK (`google-generativeai`) |
| **Database** | SQLite (Dev) / PostgreSQL 16 (Production) |
| **Analytics & Data** | Pandas 2.2, OpenPyXL 3.1 |
| **API Specs & Docs** | drf-spectacular (OpenAPI 3.0 / Swagger UI / Redoc) |
| **Containerization** | Docker, Docker Compose, Gunicorn |

---

## 📁 5. Folder Structure

```text
aiwebsite/
├── backend/
│   ├── accounts/          # User model, Subscription, Payment, JWT Auth
│   ├── users/             # UserProfile, Notification, Feedback
│   ├── nutrition/         # Food DB, FoodCategory, load_foods seeder
│   ├── mealplanner/       # MealPlan, Meal, FavoriteMeal, GroceryItem
│   ├── health/            # BMIRecord, WaterTracker, ExerciseLog, Calculators
│   ├── ai_engine/         # Gemini client, Prompt builder, Parser, Telemetry
│   ├── activity_logs/     # LoginHistory, ActivityLog, Events, Exporter, ETL
│   ├── api/               # Master URL router
│   ├── config/            # Django settings (base.py, local.py, production.py)
│   ├── exports/           # Auto-generated CSV, JSON, XLSX files
│   ├── Dockerfile
│   ├── requirements.txt
│   └── manage.py
├── frontend/              # React 18 Vite frontend application
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI pipeline
├── docker-compose.yml     # PostgreSQL + Django + React services
└── README.md
```

---

## 🚀 6. Installation & Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### Local Execution Commands

```powershell
cd backend

# Activate virtual environment
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Run Database Migrations
.\venv\Scripts\python.exe manage.py migrate

# Seed Nutrition Database (60+ foods)
.\venv\Scripts\python.exe manage.py load_foods

# Execute Test Suite
.\venv\Scripts\python.exe manage.py test

# Start Development Server
.\venv\Scripts\python.exe manage.py runserver
```

---

## 🔑 7. Environment Variables (`backend/.env`)

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Leave blank for SQLite in local dev, or add PostgreSQL URL for production:
DATABASE_URL=

# Required for AI generation:
GEMINI_API_KEY=your-gemini-api-key-here

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

---

## 🐳 8. Docker Compose Deployment

```bash
# Build and start all services (Backend, Frontend, PostgreSQL DB)
docker-compose up --build
```

Services:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **PostgreSQL**: localhost:5432

---

## 🌐 9. API Endpoints

| Method | Endpoint | Description | Throttling |
|---|---|---|---|
| `POST` | `/api/register/` | Register new user account | 10 / hour |
| `POST` | `/api/login/` | User login → JWT access & refresh pair | 10 / min |
| `POST` | `/api/token/refresh/` | Refresh JWT access token | 10 / min |
| `GET` | `/api/me/` | Authenticated user profile | 1000 / day |
| `GET/PATCH`| `/api/profile/` | Physical stats & diet preferences | 1000 / day |
| `POST` | `/api/generate-plan/` | 🤖 Generate AI diet plan with Gemini | 30 / hour |
| `GET` | `/api/meal-plans/` | Meal plan history | 1000 / day |
| `POST` | `/api/bmi/` | Calculate BMI & save progress record | 1000 / day |
| `GET/PATCH`| `/api/water/` | Today's water intake log | 1000 / day |
| `GET` | `/api/exports/` | List auto-generated CSV, JSON, XLSX exports | 1000 / day |
| `GET` | `/api/health/status/` | System status & DB health check | Public |

---

## 🛡️ 10. Security & Hardening

- **JWT Token Lifetime**: Access tokens expire in 60 minutes; refresh tokens expire in 7 days with rotation.
- **SQL Injection Defense**: All database access uses Django ORM parameterized queries.
- **XSS & Security Headers**: Includes `X-Frame-Options: DENY`, `SECURE_CONTENT_TYPE_NOSNIFF`, and HSTS configuration.
- **Secrets Isolation**: Environment variables loaded strictly via `python-decouple`.

---

## 🧪 11. Testing & Verification

Run deployment checks and unit tests:

```powershell
cd backend
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py check --deploy
.\venv\Scripts\python.exe manage.py test
```

---

## 📜 12. License

MIT License — Free for commercial, portfolio, and educational use.
