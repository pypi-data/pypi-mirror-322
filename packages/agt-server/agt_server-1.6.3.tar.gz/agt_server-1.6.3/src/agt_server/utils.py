import json
import re

def extract_first_json(json_string):
    pattern = r'\{(?:[^{}]|(?R))*\}'
    match = re.search(pattern, json_string)
    
    if match:
        try:
            return json.loads(match.group(0)) 
        except json.JSONDecodeError:
            return json_string
    return json_string