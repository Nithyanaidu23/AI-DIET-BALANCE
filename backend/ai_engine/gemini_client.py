"""
Gemini API client wrapper.
Handles retry logic, JSON extraction, and error reporting.
Uses the stable google-generativeai SDK (genai.GenerativeModel).
"""
import json
import logging
import re
import time
from typing import Optional

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger('ai_engine')

_api_configured = False


def _ensure_configured():
    """Configure the Gemini SDK once per process (thread-safe for Django)."""
    global _api_configured
    if not _api_configured:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError(
                'GEMINI_API_KEY is not set. Add it to your backend/.env file.'
            )
        genai.configure(api_key=api_key)
        _api_configured = True


def _extract_json(text: str) -> Optional[dict]:
    """
    Extract the first valid JSON object from a string.
    Handles cases where the model wraps JSON in markdown code fences.
    """
    # Strip markdown code fences if present
    text = re.sub(r'```(?:json)?\s*', '', text).strip()
    text = text.rstrip('`').strip()

    # Find JSON object boundaries
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1:
        return None

    json_str = text[start:end + 1]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.warning('JSON decode failed: %s', e)
        return None


def call_gemini(prompt: str, max_retries: int = 3, temperature: float = 0.7) -> dict:
    """
    Send a prompt to Gemini and return a parsed JSON dict.

    Raises:
        ValueError: If the API key is not configured.
        RuntimeError: If all retries fail or JSON cannot be parsed.
    """
    if getattr(settings, 'LOAD_TEST', False):
        return {
            "plan_title": "Load Test Mocked 7-Day Meal Plan",
            "total_days": 1,
            "daily_targets": {
                "calories": 2000,
                "protein_g": 150,
                "carbs_g": 200,
                "fat_g": 65,
                "water_ml": 2500,
            },
            "days": [
                {
                    "day_number": 1,
                    "day_name": "Monday",
                    "total_calories": 400,
                    "total_protein_g": 15.0,
                    "total_carbs_g": 60.0,
                    "total_fat_g": 8.0,
                    "meals": [
                        {
                            "meal_type": "breakfast",
                            "name": "Oatmeal with Berries",
                            "description": "Healthy breakfast oats",
                            "calories": 400,
                            "protein_g": 15.0,
                            "carbs_g": 60.0,
                            "fat_g": 8.0,
                            "prep_time_minutes": 5,
                            "cook_time_minutes": 5,
                            "recipe_steps": "1. Boil oats. 2. Add berries.",
                            "ingredients": ["Oats", "Blueberries", "Milk"]
                        }
                    ]
                }
            ],
            "grocery_list": [
                {
                    "name": "Oats",
                    "quantity": 1.0,
                    "unit": "kg",
                    "category": "Grains"
                }
            ],
            "notes": "This is a mock meal plan for load testing.",
            "_telemetry": {
                "latency_ms": 10.0,
                "model_name": "gemini-1.5-flash-mocked",
                "request_size_chars": len(prompt),
                "response_size_chars": 500,
                "estimated_input_tokens": 100,
                "estimated_output_tokens": 125,
                "estimated_cost_usd": 0.000045,
            }
        }

    _ensure_configured()


    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        response_mime_type='application/json',
    )

    model = genai.GenerativeModel(
        model_name=getattr(settings, 'GEMINI_MODEL', 'gemini-1.5-flash'),
        generation_config=generation_config,
    )

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            logger.debug('Gemini request attempt %d/%d', attempt, max_retries)
            start_time = time.time()
            response = model.generate_content(prompt)
            latency_ms = round((time.time() - start_time) * 1000, 2)
            raw_text = response.text

            request_size = len(prompt)
            response_size = len(raw_text)
            est_input_tokens = int(request_size / 4)
            est_output_tokens = int(response_size / 4)
            est_cost_usd = round((est_input_tokens * 0.000000075) + (est_output_tokens * 0.0000003), 6)

            telemetry = {
                'latency_ms': latency_ms,
                'model_name': getattr(settings, 'GEMINI_MODEL', 'gemini-1.5-flash'),
                'request_size_chars': request_size,
                'response_size_chars': response_size,
                'estimated_input_tokens': est_input_tokens,
                'estimated_output_tokens': est_output_tokens,
                'estimated_cost_usd': est_cost_usd,
            }

            parsed = _extract_json(raw_text)
            if parsed is not None:
                parsed['_telemetry'] = telemetry
                logger.info('Gemini response parsed successfully in %.2fms. Telemetry: %s', latency_ms, telemetry)
                return parsed


            logger.warning('Attempt %d: no valid JSON in Gemini response.', attempt)
            last_error = 'No valid JSON object found in Gemini response.'

        except Exception as exc:
            logger.error('Gemini API error on attempt %d: %s', attempt, exc)
            last_error = str(exc)

        if attempt < max_retries:
            wait = 2 ** attempt
            logger.debug('Retrying in %ds…', wait)
            time.sleep(wait)

    raise RuntimeError(
        f'Gemini call failed after {max_retries} attempts. Last error: {last_error}'
    )
