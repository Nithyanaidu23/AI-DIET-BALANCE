"""
Unit tests for health calculators.
Run with: python manage.py test health.tests
"""
from django.test import TestCase
from .calculators import (
    calculate_bmi,
    bmi_category,
    calculate_bmr,
    calculate_tdee,
    calculate_goal_calories,
    estimate_body_fat,
    ideal_weight_devine,
    macro_split,
    full_health_report,
)


class BMICalculatorTests(TestCase):

    def test_bmi_normal(self):
        bmi = calculate_bmi(weight_kg=70, height_cm=175)
        self.assertAlmostEqual(bmi, 22.9, delta=0.1)

    def test_bmi_overweight(self):
        bmi = calculate_bmi(weight_kg=90, height_cm=170)
        self.assertAlmostEqual(bmi, 31.1, delta=0.1)

    def test_bmi_zero_height_raises(self):
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)

    def test_bmi_category_underweight(self):
        self.assertEqual(bmi_category(17.0), 'Underweight')

    def test_bmi_category_normal(self):
        self.assertEqual(bmi_category(22.0), 'Normal weight')

    def test_bmi_category_overweight(self):
        self.assertEqual(bmi_category(27.0), 'Overweight')

    def test_bmi_category_obese(self):
        self.assertEqual(bmi_category(35.0), 'Obese')


class BMRCalculatorTests(TestCase):

    def test_bmr_male(self):
        bmr = calculate_bmr(weight_kg=80, height_cm=180, age=30, gender='male')
        # 10*80 + 6.25*180 - 5*30 + 5 = 800 + 1125 - 150 + 5 = 1780
        self.assertAlmostEqual(bmr, 1780, delta=5)

    def test_bmr_female(self):
        bmr = calculate_bmr(weight_kg=60, height_cm=165, age=25, gender='female')
        # 10*60 + 6.25*165 - 5*25 - 161 = 600 + 1031.25 - 125 - 161 = 1345.25
        self.assertAlmostEqual(bmr, 1345, delta=5)


class TDEETests(TestCase):

    def test_tdee_sedentary(self):
        tdee = calculate_tdee(bmr=1780, activity_level='sedentary')
        self.assertAlmostEqual(tdee, 1780 * 1.2, delta=10)

    def test_tdee_moderate(self):
        tdee = calculate_tdee(bmr=1780, activity_level='moderate')
        self.assertAlmostEqual(tdee, 1780 * 1.55, delta=10)

    def test_goal_calories_lose_fat(self):
        tdee = 2500
        gc = calculate_goal_calories(tdee, 'lose_fat')
        self.assertEqual(gc, 2000)

    def test_goal_calories_never_below_1200(self):
        gc = calculate_goal_calories(tdee=1500, goal='lose_fat')
        self.assertGreaterEqual(gc, 1200)


class MacroSplitTests(TestCase):

    def test_macro_split_lose_fat_sums_correctly(self):
        macros = macro_split(2000, 'lose_fat')
        total_kcal = macros['protein_g'] * 4 + macros['carbs_g'] * 4 + macros['fat_g'] * 9
        # Allow ±5% tolerance
        self.assertAlmostEqual(total_kcal, 2000, delta=100)

    def test_macro_split_build_muscle_high_carbs(self):
        macros = macro_split(2500, 'build_muscle')
        self.assertGreater(macros['carbs_g'], macros['protein_g'])


class IdealWeightTests(TestCase):

    def test_ideal_weight_male_170cm(self):
        iw = ideal_weight_devine(height_cm=170, gender='male')
        # 170cm = 66.9 inches; over_5_feet = 6.9 inches; 50 + 2.3*6.9 = 65.87
        self.assertAlmostEqual(iw, 65.9, delta=0.5)

    def test_ideal_weight_female(self):
        iw = ideal_weight_devine(height_cm=160, gender='female')
        self.assertGreater(iw, 40)
        self.assertLess(iw, 70)


class FullHealthReportTests(TestCase):

    def test_full_report_keys(self):
        report = full_health_report(
            weight_kg=72, height_cm=175, age=25,
            gender='male', activity_level='moderate', goal='lose_fat'
        )
        expected_keys = ['bmi', 'bmi_category', 'bmr', 'tdee', 'goal_calories',
                         'body_fat_percent', 'ideal_weight_kg', 'water_intake_ml',
                         'protein_g', 'carbs_g', 'fat_g']
        for key in expected_keys:
            self.assertIn(key, report)

    def test_full_report_sensible_values(self):
        report = full_health_report(
            weight_kg=72, height_cm=175, age=25,
            gender='male', activity_level='moderate', goal='lose_fat'
        )
        self.assertGreater(report['goal_calories'], 1200)
        self.assertLess(report['goal_calories'], 5000)
        self.assertGreater(report['bmi'], 0)


from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()


class HealthAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='health_api@example.com', password='Password123!')
        self.client.force_authenticate(user=self.user)

    def test_bmi_api_post(self):
        payload = {
            'weight_kg': 72.0,
            'height_cm': 175.0,
            'age': 25,
            'gender': 'male',
            'activity_level': 'moderate',
            'goal': 'lose_fat',
            'save_record': True,
        }
        res = self.client.post('/api/bmi/', payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn('bmi', res.data)

    def test_water_tracker_api(self):
        res = self.client.get('/api/water/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('amount_ml', res.data)

        # Update water
        res_update = self.client.patch('/api/water/', {'amount_ml': 1500})
        self.assertEqual(res_update.status_code, 200)
        self.assertEqual(res_update.data['amount_ml'], 1500)

