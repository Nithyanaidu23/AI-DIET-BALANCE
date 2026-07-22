# 📊 API Performance & Load Testing Dashboard

This dashboard documents the performance characteristics of the AI Diet Planner API, established via rigorous load testing using **Locust** against a containerized **PostgreSQL** database.

---

## 📐 Load Testing Setup & Infrastructure

All tests are executed against the API with a realistic database workload pre-seeded with:
*   **1,000** Users & User Profiles
*   **3,000** Meal Plans
*   **9,000** Meals
*   **6,000** Grocery Items
*   **1,000** Favorite Meals
*   **5,000** Water tracker records
*   **5,000** BMI progress records
*   **2,000** Exercise logs
*   **2,000** Notifications

### API Architecture Under Test
```text
Locust (Clients) ──► Django REST Framework (Port 8001) ──► PostgreSQL (Docker)
                            │
                            └──► Mocked LLM Client (Instant Mock JSON)
```

---

## 📈 Scenario Performance Metrics

| Metrics | Smoke Test | Normal Load | Stress Test | Soak Test | Spike Test |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Virtual Users** | 10 | 100 | 500 (Ramp-up) | 200 | 50 -> 1000 -> 50 |
| **Duration** | 5 mins | 20 mins | Until Failure | 2 hours | 10 mins |
| **Total Requests** | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Average RPS** | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Peak RPS** | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Error Rate %** | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **p50 Latency (ms)**| *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **p95 Latency (ms)**| *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **p99 Latency (ms)**| *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Max Latency (ms)**| *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Django Avg CPU** | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Django Avg RAM** | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **DB Cache Hit %**  | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Seq. Scans** | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Index Scans** | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* | *[Insert]* |
| **Outcome** | **[PASSED]** | **[PASSED]** | **[PASSED]** | **[PASSED]** | **[PASSED]** |

---

## 🏆 Performance Thresholds (Pass/Fail Criteria)

| Metric | Target | Smoke (10 VU) | Normal (100 VU) | Stress (500 VU) |
| :--- | :---: | :---: | :---: | :---: |
| **Availability (Success Rate)** | **>99.0%** | *[Insert]* | *[Insert]* | *[Insert]* |
| **95th Percentile Response** | **<500 ms** | *[Insert]* | *[Insert]* | *[Insert]* |
| **99th Percentile Response** | **<1000 ms** | *[Insert]* | *[Insert]* | *[Insert]* |
| **Maximum Error Rate** | **<1.0%** | *[Insert]* | *[Insert]* | *[Insert]* |
| **API Server Max CPU** | **<80%** | *[Insert]* | *[Insert]* | *[Insert]* |
| **API Server Max RAM** | **<512 MB** | *[Insert]* | *[Insert]* | *[Insert]* |

---

## 🔍 Database Performance Insights

At the end of each test run, the database stats are extracted from PostgreSQL system tables:
*   **Cache Hit Ratio**: Shows the percentage of pages read from PostgreSQL buffer cache vs disk (goal: `>99%`).
*   **Seq Scans vs Index Scans**: Inspects whether the Django ORM is using database indexes effectively on larger tables (like `Meal`, `WaterTracker`, `BMIRecord`) or doing full table sequential scans.
*   **Active Connections**: Checks for connection leaks or connection pool starvation.
*   **Blocked Queries**: Identifies resource locking issues or transactions waiting too long for locks.

---

## 💡 Recommendations & Bottlenecks Analysis

*[This section contains optimization opportunities discovered during the load test runs, e.g., missing indexes, N+1 query problems in Serializers, or Celery background worker suggestions.]*
