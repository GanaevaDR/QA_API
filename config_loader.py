import json
import os
from pathlib import Path

def load_credentials():
    """Load credentials from JSON file"""
    try:
        current_dir = Path(__file__).parent
        credentials_path = current_dir / 'credentials.json'
        
        if not credentials_path.exists():
            raise FileNotFoundError("credentials.json not found. Create it from credentials.template.json")
        
        with open(credentials_path, 'r') as file:
            return json.load(file)
            
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise Exception(f"Error loading credentials: {e}")

def get_credential(key, default=None):
    """Get specific credential with optional default"""
    creds = load_credentials()
    return creds.get(key, default)

