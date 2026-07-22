"""
Pure Python health calculators.
No AI — all results are deterministic and unit-testable.
"""
from decimal import Decimal


# ─── Activity multipliers (Mifflin-St Jeor / Harris-Benedict convention) ─────
ACTIVITY_MULTIPLIERS = {
    'sedentary': 1.2,
    'light': 1.375,
    'moderate': 1.55,
    'very': 1.725,
    'extra': 1.9,
}

# ─── Goal calorie adjustments ─────────────────────────────────────────────────
GOAL_ADJUSTMENTS = {
    'lose_fat': -500,
    'build_muscle': +300,
    'maintain': 0,
    'improve_health': -200,
    'increase_endurance': +200,
}


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate Body Mass Index."""
    if height_cm <= 0:
        raise ValueError('Height must be greater than 0.')
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def bmi_category(bmi: float) -> str:
    """Return BMI category string."""
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25.0:
        return 'Normal weight'
    elif bmi < 30.0:
        return 'Overweight'
    else:
        return 'Obese'


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Mifflin-St Jeor equation for Basal Metabolic Rate.
    gender: 'male' | 'female' | 'other' (defaults to average)
    """
    base = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    if gender == 'male':
        return round(base + 5, 1)
    elif gender == 'female':
        return round(base - 161, 1)
    else:
        # Average of male and female
        return round(base - 78, 1)


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Total Daily Energy Expenditure = BMR × activity multiplier."""
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
    return round(bmr * multiplier, 0)


def calculate_goal_calories(tdee: float, goal: str) -> float:
    """Adjust TDEE based on the user's fitness goal."""
    adjustment = GOAL_ADJUSTMENTS.get(goal, 0)
    return max(1200, round(tdee + adjustment, 0))  # never below 1200 kcal


def estimate_body_fat(bmi: float, age: int, gender: str) -> float:
    """
    BMI-based body fat estimation (Deurenberg formula).
    Not as accurate as DEXA but gives a useful approximation.
    """
    gender_factor = 1 if gender == 'male' else 0
    bf = (1.20 * bmi) + (0.23 * age) - (10.8 * gender_factor) - 5.4
    return round(max(5.0, bf), 1)


def ideal_weight_devine(height_cm: float, gender: str) -> float:
    """
    Devine formula for ideal body weight.
    Returns weight in kg.
    """
    height_inches = height_cm / 2.54
    inches_over_5_feet = max(0, height_inches - 60)
    if gender == 'male':
        return round(50.0 + 2.3 * inches_over_5_feet, 1)
    else:
        return round(45.5 + 2.3 * inches_over_5_feet, 1)


def macro_split(goal_calories: float, goal: str) -> dict:
    """
    Recommended macro split (grams) based on fitness goal.
    Returns protein_g, carbs_g, fat_g.
    """
    splits = {
        'lose_fat':       {'protein': 0.40, 'carbs': 0.30, 'fat': 0.30},
        'build_muscle':   {'protein': 0.30, 'carbs': 0.45, 'fat': 0.25},
        'maintain':       {'protein': 0.25, 'carbs': 0.50, 'fat': 0.25},
        'improve_health': {'protein': 0.25, 'carbs': 0.50, 'fat': 0.25},
        'increase_endurance': {'protein': 0.20, 'carbs': 0.55, 'fat': 0.25},
    }
    s = splits.get(goal, splits['maintain'])
    return {
        'protein_g': round(goal_calories * s['protein'] / 4, 0),   # 4 kcal/g
        'carbs_g':   round(goal_calories * s['carbs'] / 4, 0),
        'fat_g':     round(goal_calories * s['fat'] / 9, 0),        # 9 kcal/g
    }


def recommended_water_intake_ml(weight_kg: float, activity_level: str) -> int:
    """Rule of thumb: 35ml/kg, +500ml for moderate/very/extra activity."""
    base_ml = weight_kg * 35
    if activity_level in ('moderate', 'very', 'extra'):
        base_ml += 500
    return int(round(base_ml, -50))  # round to nearest 50ml


def full_health_report(weight_kg: float, height_cm: float, age: int, gender: str,
                        activity_level: str, goal: str) -> dict:
    """
    Single function that returns a complete health profile.
    Used by both /api/bmi/ and /api/calorie/ endpoints.
    """
    bmi = calculate_bmi(weight_kg, height_cm)
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    goal_calories = calculate_goal_calories(tdee, goal)
    macros = macro_split(goal_calories, goal)
    body_fat = estimate_body_fat(bmi, age, gender)
    ideal_weight = ideal_weight_devine(height_cm, gender)
    water_ml = recommended_water_intake_ml(weight_kg, activity_level)

    return {
        'bmi': bmi,
        'bmi_category': bmi_category(bmi),
        'bmr': bmr,
        'tdee': tdee,
        'goal_calories': goal_calories,
        'body_fat_percent': body_fat,
        'ideal_weight_kg': ideal_weight,
        'water_intake_ml': water_ml,
        **macros,
    }
