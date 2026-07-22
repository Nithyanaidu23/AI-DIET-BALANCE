"""
Response parser and validator.
Validates and coerces Gemini's JSON output to a strict schema.
"""
from typing import Any


class ValidationError(Exception):
    pass


def _require(d: dict, key: str, expected_type=None, default=None) -> Any:
    val = d.get(key, default)
    if val is None:
        raise ValidationError(f'Missing required field: {key}')
    if expected_type is not None and not isinstance(val, expected_type):
        try:
            val = expected_type(val)
        except (TypeError, ValueError):
            raise ValidationError(f'Field "{key}" must be of type {expected_type.__name__}, got {type(val).__name__}')
    return val


VALID_MEAL_TYPES = {'breakfast', 'lunch', 'dinner', 'snack', 'pre_workout', 'post_workout'}


def validate_meal(meal: dict, day_num: int, meal_idx: int) -> dict:
    prefix = f'Day {day_num}, meal {meal_idx}'
    meal_type = str(meal.get('meal_type', 'snack')).lower()
    if meal_type not in VALID_MEAL_TYPES:
        meal_type = 'snack'

    return {
        'meal_type': meal_type,
        'name': str(meal.get('name', 'Unnamed Meal'))[:200],
        'description': str(meal.get('description', ''))[:500],
        'calories': max(0, int(meal.get('calories', 0))),
        'protein_g': max(0, float(meal.get('protein_g', 0))),
        'carbs_g': max(0, float(meal.get('carbs_g', 0))),
        'fat_g': max(0, float(meal.get('fat_g', 0))),
        'prep_time_minutes': int(meal.get('prep_time_minutes', 0)),
        'cook_time_minutes': int(meal.get('cook_time_minutes', 0)),
        'recipe_steps': str(meal.get('recipe_steps', '')),
        'ingredients': [str(i) for i in meal.get('ingredients', [])],
    }


def validate_day(day: dict, idx: int) -> dict:
    day_number = int(day.get('day_number', idx + 1))
    meals_raw = day.get('meals', [])
    if not isinstance(meals_raw, list) or len(meals_raw) == 0:
        raise ValidationError(f'Day {day_number} has no meals.')

    meals = [validate_meal(m, day_number, i) for i, m in enumerate(meals_raw)]

    return {
        'day_number': day_number,
        'day_name': str(day.get('day_name', f'Day {day_number}')),
        'total_calories': int(day.get('total_calories', sum(m['calories'] for m in meals))),
        'total_protein_g': float(day.get('total_protein_g', sum(m['protein_g'] for m in meals))),
        'total_carbs_g': float(day.get('total_carbs_g', sum(m['carbs_g'] for m in meals))),
        'total_fat_g': float(day.get('total_fat_g', sum(m['fat_g'] for m in meals))),
        'meals': meals,
    }


def validate_grocery_item(item: dict) -> dict:
    return {
        'name': str(item.get('name', 'Unknown'))[:200],
        'quantity': float(item.get('quantity', 1)),
        'unit': str(item.get('unit', 'piece'))[:50],
        'category': str(item.get('category', 'Other'))[:100],
    }


def validate_and_parse(raw: dict) -> dict:
    """
    Validate and normalise the raw Gemini response.
    Returns a clean, typed dict ready for DB persistence.

    Raises ValidationError on structural problems.
    """
    if not isinstance(raw, dict):
        raise ValidationError('Response must be a JSON object.')

    days_raw = raw.get('days', [])
    if not isinstance(days_raw, list) or len(days_raw) == 0:
        raise ValidationError('Response must contain a "days" array with at least one entry.')

    days = [validate_day(d, i) for i, d in enumerate(days_raw)]

    daily_targets = raw.get('daily_targets', {})
    grocery_raw = raw.get('grocery_list', [])
    grocery = [validate_grocery_item(g) for g in grocery_raw if isinstance(g, dict)]

    return {
        'plan_title': str(raw.get('plan_title', '7-Day Meal Plan'))[:200],
        'total_days': len(days),
        'daily_targets': {
            'calories': int(daily_targets.get('calories', 2000)),
            'protein_g': int(daily_targets.get('protein_g', 150)),
            'carbs_g': int(daily_targets.get('carbs_g', 200)),
            'fat_g': int(daily_targets.get('fat_g', 65)),
            'water_ml': int(daily_targets.get('water_ml', 2500)),
        },
        'days': days,
        'grocery_list': grocery,
        'notes': str(raw.get('notes', '')),
    }
