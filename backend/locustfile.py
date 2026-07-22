import uuid
import random
from locust import HttpUser, task, between, tag

class DietPlannerUser(HttpUser):
    # Wait between 1 and 3 seconds between tasks to simulate human behavior
    wait_time = between(1, 3)

    def on_start(self):
        """
        Runs when a virtual user is spawned.
        Picks one of the 1000 pre-seeded users and logs in to cache the JWT token.
        Falls back to registration if login fails (e.g. if database is not seeded).
        """
        user_idx = random.randint(1, 1000)
        self.email = f"loadtest_{user_idx:04d}@example.com"
        self.password = "LoadTestPass123!"
        self.headers = {}
        self.auth_failed = False
        
        login_payload = {
            "email": self.email,
            "password": self.password
        }
        with self.client.post("/api/login/", json=login_payload, catch_response=True) as response:
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access")
                self.headers = {"Authorization": f"Bearer {self.access_token}"}
                response.success()
            else:
                # Fallback: Register a new user dynamically if pre-seeded users do not exist
                response.success() # Clear the error status on the login try
                self.register_and_login_fallback()

    def register_and_login_fallback(self):
        """Helper fallback to register a new user dynamically."""
        username = f"fallback_{uuid.uuid4().hex[:10]}"
        self.email = f"{username}@example.com"
        self.password = "LoadTestPass123!"
        
        register_payload = {
            "email": self.email,
            "first_name": "Fallback",
            "last_name": "Tester",
            "password": self.password,
            "password2": self.password
        }
        
        with self.client.post("/api/register/", json=register_payload, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Fallback signup failed: {response.text}")
                self.auth_failed = True
                return

        login_payload = {
            "email": self.email,
            "password": self.password
        }
        with self.client.post("/api/login/", json=login_payload, catch_response=True) as response:
            if response.status_code == 200:
                self.access_token = response.json().get("access")
                self.headers = {"Authorization": f"Bearer {self.access_token}"}
                response.success()
            else:
                response.failure(f"Fallback login failed: {response.text}")
                self.auth_failed = True

    # ──────────────────────────────────────────────────────────────────────────
    # Task 1: Fetch Dashboard (30% weight)
    # ──────────────────────────────────────────────────────────────────────────
    @tag('dashboard')
    @task(30)
    def test_dashboard(self):
        if self.auth_failed or not self.headers:
            return
        self.client.get("/api/dashboard/", headers=self.headers)

    # ──────────────────────────────────────────────────────────────────────────
    # Task 2: Generate Meal (20% weight)
    # ──────────────────────────────────────────────────────────────────────────
    @tag('generate_meal')
    @task(20)
    def test_generate_meal(self):
        if self.auth_failed or not self.headers:
            return
        generate_payload = {
            "weight_kg": round(random.uniform(60.0, 95.0), 1),
            "height_cm": round(random.uniform(160.0, 190.0), 1),
            "age": random.randint(20, 50),
            "gender": random.choice(["male", "female", "other"]),
            "activity_level": random.choice(['sedentary', 'light', 'moderate', 'very', 'extra']),
            "goal": random.choice(['lose_fat', 'build_muscle', 'maintain', 'improve_health']),
            "food_preference": random.choice(["none", "vegetarian", "vegan"]),
            "cuisine_preference": random.choice(["Italian", "Indian", "Mexican", "Asian", ""]),
            "budget_per_day_usd": random.randint(10, 30)
        }
        self.client.post("/api/generate-plan/", json=generate_payload, headers=self.headers)

    # ──────────────────────────────────────────────────────────────────────────
    # Task 3: Search Foods (15% weight)
    # ──────────────────────────────────────────────────────────────────────────
    @tag('search_foods')
    @task(15)
    def test_search_foods(self):
        params = {
            "search": random.choice(["Oats", "Chicken", "Sweet Potato", "Salmon", "Egg", "Almonds", "Apple", "Banana", ""]),
            "is_vegetarian": random.choice(["true", "false", ""]),
            "is_vegan": random.choice(["true", "false", ""]),
            "max_calories": random.choice([200, 400, 600, ""])
        }
        params = {k: v for k, v in params.items() if v != ""}
        # We query the food directory. SinceIsAuthenticatedOrReadOnly is set, we don't strictly need headers, 
        # but let's send them if we have them to test both paths.
        self.client.get("/api/foods/", params=params, headers=self.headers)

    # ──────────────────────────────────────────────────────────────────────────
    # Task 4: Water Tracker (10% weight)
    # ──────────────────────────────────────────────────────────────────────────
    @tag('water')
    @task(10)
    def test_water_tracker(self):
        if self.auth_failed or not self.headers:
            return
        
        # Get current state
        self.client.get("/api/water/", headers=self.headers)
        
        # Update water intake with random amount
        patch_payload = {
            "amount_ml": random.randint(250, 3000)
        }
        self.client.patch("/api/water/", json=patch_payload, headers=self.headers)

    # ──────────────────────────────────────────────────────────────────────────
    # Task 5: BMI Tracking (10% weight)
    # ──────────────────────────────────────────────────────────────────────────
    @tag('bmi')
    @task(10)
    def test_bmi_flow(self):
        if self.auth_failed or not self.headers:
            return
        
        # Get history
        self.client.get("/api/bmi/history/", params={"days": random.choice([30, 90])}, headers=self.headers)
        
        # Post new BMI calculation (and save it 50% of the time)
        bmi_payload = {
            "weight_kg": round(random.uniform(55.0, 100.0), 1),
            "height_cm": round(random.uniform(150.0, 195.0), 1),
            "age": random.randint(18, 65),
            "gender": random.choice(["male", "female", "other"]),
            "activity_level": random.choice(['sedentary', 'light', 'moderate', 'very', 'extra']),
            "goal": random.choice(['lose_fat', 'build_muscle', 'maintain', 'improve_health']),
            "save_record": random.choice([True, False])
        }
        self.client.post("/api/bmi/", json=bmi_payload, headers=self.headers)

    # ──────────────────────────────────────────────────────────────────────────
    # Task 6: Meal History & Detail Views (10% weight)
    # ──────────────────────────────────────────────────────────────────────────
    @tag('meal_history')
    @task(10)
    def test_meal_history(self):
        if self.auth_failed or not self.headers:
            return
            
        # Get history list
        with self.client.get("/api/meal-plans/", headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                plans = response.json()
                # If plans are returned, hit a detail and grocery view for a random plan
                if isinstance(plans, list) and len(plans) > 0:
                    plan = random.choice(plans)
                    plan_id = plan.get('id')
                    if plan_id:
                        self.client.get(f"/api/meal-plans/{plan_id}/", headers=self.headers)
                        self.client.get(f"/api/meal-plans/{plan_id}/grocery/", headers=self.headers)
                        # Toggle favorite occasionally (50% chance)
                        if random.choice([True, False]):
                            self.client.post(f"/api/meal-plans/{plan_id}/favorite/", headers=self.headers)
                response.success()
            else:
                response.failure(f"Failed to fetch meal plan history: {response.status_code}")

    # ──────────────────────────────────────────────────────────────────────────
    # Task 7: Profile Update (5% weight)
    # ──────────────────────────────────────────────────────────────────────────
    @tag('profile')
    @task(5)
    def test_profile_update(self):
        if self.auth_failed or not self.headers:
            return
        
        patch_payload = {
            "weight_kg": round(random.uniform(60.0, 95.0), 1),
            "activity_level": random.choice(['sedentary', 'light', 'moderate', 'very', 'extra']),
            "fitness_goal": random.choice(['lose_fat', 'build_muscle', 'maintain', 'improve_health'])
        }
        self.client.patch("/api/profile/", json=patch_payload, headers=self.headers)

    # ──────────────────────────────────────────────────────────────────────────
    # Task 8: Dynamic Signups (2% weight)
    # ──────────────────────────────────────────────────────────────────────────
    @tag('signup')
    @task(2)
    def test_dynamic_signup_flow(self):
        """Simulates dynamic new users joining the platform."""
        username = f"loadtest_dynamic_{uuid.uuid4().hex[:8]}"
        email = f"{username}@example.com"
        password = "LoadTestPass123!"
        
        # Register
        register_payload = {
            "email": email,
            "first_name": "Dynamic",
            "last_name": "User",
            "password": password,
            "password2": password
        }
        with self.client.post("/api/register/", json=register_payload, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Dynamic signup registration failed: {response.text}")
                return
                
        # Login
        login_payload = {
            "email": email,
            "password": password
        }
        with self.client.post("/api/login/", json=login_payload, catch_response=True) as response:
            if response.status_code == 200:
                # Update headers to simulate this new user performing subsequent tasks!
                token_data = response.json()
                self.access_token = token_data.get("access")
                self.headers = {"Authorization": f"Bearer {self.access_token}"}
                response.success()
            else:
                response.failure(f"Dynamic signup login failed: {response.text}")
