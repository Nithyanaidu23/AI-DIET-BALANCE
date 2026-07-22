import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserProfile, Notification
from health.models import BMIRecord, WaterTracker, ExerciseLog
from mealplanner.models import MealPlan, Meal, GroceryItem, FavoriteMeal, MealType
from nutrition.models import Food

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds a comprehensive dataset (users, profiles, meal plans, metrics) for load testing.'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=1000, help='Number of users to seed')

    def handle(self, *args, **options):
        count = options['count']
        password = "LoadTestPass123!"
        self.stdout.write(f"Seeding {count} users and related records for load testing...")

        # 1. Create Users
        users_to_create = []
        existing_emails = set(User.objects.filter(email__startswith="loadtest_").values_list('email', flat=True))
        
        for i in range(1, count + 1):
            email = f"loadtest_{i:04d}@example.com"
            if email not in existing_emails:
                user = User(
                    email=email,
                    first_name=f"Load{i}",
                    last_name="Tester",
                    is_active=True
                )
                user.set_password(password)
                users_to_create.append(user)
                
        if users_to_create:
            User.objects.bulk_create(users_to_create)
            self.stdout.write(f"Created {len(users_to_create)} users.")
        
        # Reload users to get IDs
        load_users = list(User.objects.filter(email__startswith="loadtest_"))
        
        # 2. User Profiles
        existing_profiles = set(UserProfile.objects.filter(user__in=load_users).values_list('user_id', flat=True))
        profiles_to_create = []
        for u in load_users:
            if u.id not in existing_profiles:
                profiles_to_create.append(UserProfile(
                    user=u,
                    weight_kg=random.choice([65.0, 70.0, 75.0, 80.0, 85.0]),
                    height_cm=random.choice([165.0, 170.0, 175.0, 180.0, 185.0]),
                    age=random.randint(20, 50),
                    gender=random.choice(['male', 'female', 'other']),
                    activity_level=random.choice(['sedentary', 'light', 'moderate', 'very', 'extra']),
                    fitness_goal=random.choice(['lose_fat', 'build_muscle', 'maintain', 'improve_health']),
                    is_complete=True
                ))
        if profiles_to_create:
            UserProfile.objects.bulk_create(profiles_to_create)
            self.stdout.write(f"Created {len(profiles_to_create)} UserProfiles.")

        # 3. Water Trackers (5 per user for the last 5 days)
        self.stdout.write("Seeding Water Logs...")
        existing_water = set(WaterTracker.objects.filter(user__in=load_users).values_list('user_id', 'date'))
        water_to_create = []
        today = date.today()
        for u in load_users:
            for d_offset in range(5):
                d = today - timedelta(days=d_offset)
                if (u.id, d) not in existing_water:
                    water_to_create.append(WaterTracker(
                        user=u,
                        date=d,
                        amount_ml=random.randint(1000, 3000),
                        target_ml=2500
                    ))
        if water_to_create:
            WaterTracker.objects.bulk_create(water_to_create, ignore_conflicts=True)
            self.stdout.write(f"Created {len(water_to_create)} WaterTracker logs.")

        # 4. BMI Records (5 per user, spaced out by 10 days)
        self.stdout.write("Seeding BMI Records...")
        existing_bmi_count = BMIRecord.objects.filter(user__in=load_users).count()
        if existing_bmi_count < count * 3:
            bmi_to_create = []
            for u in load_users:
                base_weight = random.uniform(60.0, 90.0)
                height = 175.0
                for j in range(5):
                    # Simulating weight progress
                    weight = base_weight + (j * random.uniform(-0.5, 0.5))
                    bmi = weight / ((height / 100) ** 2)
                    bmi_to_create.append(BMIRecord(
                        user=u,
                        weight_kg=round(weight, 1),
                        height_cm=height,
                        bmi=round(bmi, 1),
                        bmi_category="Normal weight",
                        body_fat_percent=18.0,
                        ideal_weight_kg=70.0,
                        goal_calories=2200
                    ))
            BMIRecord.objects.bulk_create(bmi_to_create)
            self.stdout.write(f"Created {len(bmi_to_create)} BMI records.")

        # 5. Exercise Logs (2 per user)
        self.stdout.write("Seeding Exercise Logs...")
        existing_exercise_count = ExerciseLog.objects.filter(user__in=load_users).count()
        if existing_exercise_count < count * 2:
            exercise_to_create = []
            exercises = ["Running", "Cycling", "Swimming", "Weightlifting", "Yoga"]
            for u in load_users:
                for _ in range(2):
                    exercise_to_create.append(ExerciseLog(
                        user=u,
                        exercise_name=random.choice(exercises),
                        duration_minutes=random.choice([30, 45, 60]),
                        calories_burned=random.randint(200, 600)
                    ))
            ExerciseLog.objects.bulk_create(exercise_to_create)
            self.stdout.write(f"Created {len(exercise_to_create)} Exercise logs.")

        # 6. Notifications (2 per user)
        self.stdout.write("Seeding Notifications...")
        existing_notif_count = Notification.objects.filter(user__in=load_users).count()
        if existing_notif_count < count * 2:
            notifs_to_create = []
            for u in load_users:
                notifs_to_create.append(Notification(
                    user=u,
                    title="Welcome to AI Diet Planner!",
                    message="Your load test account is successfully set up and active.",
                    is_read=random.choice([True, False])
                ))
                notifs_to_create.append(Notification(
                    user=u,
                    title="Daily Goal Reached!",
                    message="Congratulations, you hit your daily water intake goal yesterday.",
                    is_read=random.choice([True, False])
                ))
            Notification.objects.bulk_create(notifs_to_create)
            self.stdout.write(f"Created {len(notifs_to_create)} Notifications.")

        # 7. Meal Plans & Meals (3 meal plans per user, with 3 meals each)
        self.stdout.write("Seeding Meal Plans and Meals...")
        existing_plans_count = MealPlan.objects.filter(user__in=load_users).count()
        if existing_plans_count < count * 2:
            plans_to_create = []
            for u in load_users:
                for plan_idx in range(3):
                    plans_to_create.append(MealPlan(
                        user=u,
                        title=f"7-Day Plan {plan_idx + 1}",
                        start_date=today - timedelta(days=plan_idx * 7),
                        end_date=today - timedelta(days=plan_idx * 7 - 6),
                        target_calories=2000,
                        target_protein_g=150,
                        target_carbs_g=200,
                        target_fat_g=65,
                        target_water_ml=2500,
                        ai_generated=True,
                        notes="Auto-seeded for performance load testing"
                    ))
            
            MealPlan.objects.bulk_create(plans_to_create)
            self.stdout.write(f"Created {len(plans_to_create)} MealPlans.")
            
            # Retrieve created plans to get their IDs
            created_plans = list(MealPlan.objects.filter(user__in=load_users))
            
            meals_to_create = []
            groceries_to_create = []
            
            for plan in created_plans:
                # Add breakfast, lunch, dinner for day 1
                meals_to_create.append(Meal(
                    meal_plan=plan,
                    meal_type=MealType.BREAKFAST,
                    day_number=1,
                    name="Oatmeal with Almonds",
                    description="Oats topped with sliced almonds",
                    calories=450,
                    protein_g=15.0,
                    carbs_g=60.0,
                    fat_g=12.0,
                    recipe_steps="1. Cook oats in water. 2. Stir in almonds.",
                    prep_time_minutes=5,
                    cook_time_minutes=5
                ))
                meals_to_create.append(Meal(
                    meal_plan=plan,
                    meal_type=MealType.LUNCH,
                    day_number=1,
                    name="Grilled Chicken Salad",
                    description="Chicken breast over green salad with vinaigrette",
                    calories=600,
                    protein_g=45.0,
                    carbs_g=15.0,
                    fat_g=20.0,
                    recipe_steps="1. Grill chicken. 2. Toss veggies. 3. Slice chicken and place on salad.",
                    prep_time_minutes=10,
                    cook_time_minutes=15
                ))
                meals_to_create.append(Meal(
                    meal_plan=plan,
                    meal_type=MealType.DINNER,
                    day_number=1,
                    name="Salmon with Sweet Potato",
                    description="Baked salmon with roasted sweet potato cubes",
                    calories=750,
                    protein_g=40.0,
                    carbs_g=50.0,
                    fat_g=25.0,
                    recipe_steps="1. Bake salmon at 400F. 2. Roast sweet potato cubes.",
                    prep_time_minutes=10,
                    cook_time_minutes=25
                ))
                
                # Add grocery items
                groceries_to_create.append(GroceryItem(
                    meal_plan=plan,
                    name="Oats",
                    quantity=1.0,
                    unit="kg",
                    category="Grains"
                ))
                groceries_to_create.append(GroceryItem(
                    meal_plan=plan,
                    name="Chicken Breast",
                    quantity=500.0,
                    unit="g",
                    category="Meat/Poultry"
                ))

            if meals_to_create:
                Meal.objects.bulk_create(meals_to_create)
                self.stdout.write(f"Created {len(meals_to_create)} Meals.")
                
            if groceries_to_create:
                GroceryItem.objects.bulk_create(groceries_to_create)
                self.stdout.write(f"Created {len(groceries_to_create)} GroceryItems.")

            # 8. Favorite Meals (1 per user linking their first plan)
            self.stdout.write("Seeding Favorites...")
            existing_favs = set(FavoriteMeal.objects.filter(user__in=load_users).values_list('user_id', flat=True))
            favs_to_create = []
            
            user_plan_map = {}
            for plan in created_plans:
                if plan.user_id not in user_plan_map:
                    user_plan_map[plan.user_id] = plan
                    
            for u in load_users:
                if u.id not in existing_favs and u.id in user_plan_map:
                    favs_to_create.append(FavoriteMeal(
                        user=u,
                        meal_plan=user_plan_map[u.id],
                        note="Seeded favorite"
                    ))
            if favs_to_create:
                FavoriteMeal.objects.bulk_create(favs_to_create)
                self.stdout.write(f"Created {len(favs_to_create)} FavoriteMeal records.")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully! All performance test data is ready."))
