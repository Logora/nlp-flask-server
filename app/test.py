from app import argument_summary_analysis
from seeds import arguments
import requests
import json

url = 'http://localhost:8000/analysis'
params = {
    'uid': 'argument-summary-9520-1',
    'name': 'argument_summary',
    'question': arguments["question"],
}

body = {
    'documents': arguments["first_position"]
}
response = requests.post(url, params=params, json=body)
print(response.json())