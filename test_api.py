"""Simple test script to verify OPENWEATHER_API_KEY and call the helper.

Usage:
    python test_api.py

This script reads `OPENWEATHER_API_KEY` from the environment or .env file and calls `get_current_weather` for a quick smoke test.
"""
import os
from dotenv import load_dotenv
from weather import get_current_weather

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not API_KEY:
    print('OPENWEATHER_API_KEY not set. Create a .env or set the environment variable.')
    raise SystemExit(1)

city = 'London'
print(f'Testing API key by fetching weather for {city}...')
res = get_current_weather(city, API_KEY, units='metric')

if res.get('error'):
    print('Error from API:', res['error'])
    raise SystemExit(2)

data = res['data']
print('OK — got data:')
print('Location:', data.get('name'), data.get('country'))
print('Temp:', data.get('temp'))
print('Condition:', data.get('description'))
# print raw json summary
print('\nRaw keys:', ', '.join(sorted(data.get('raw', {}).keys())))
