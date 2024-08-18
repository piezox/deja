import boto3
import json
from typing import Dict, Any
import os

def load_config(config_file: str = 'qconfig.json', template_file: str = 'qconfig.template.json') -> Dict[str, Any]:
    """
    Load the AWS Q configuration from a JSON file, falling back to a template if the main file doesn't exist.
    """
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    template_path = os.path.join(os.path.dirname(__file__), template_file)
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if any(not value for value in config.values()):
            print(f"Warning: Some values in '{config_file}' are empty. Please fill them in.")
        
        return config
    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found. Using template '{template_file}'.")
        return _create_config_from_template(config_path, template_path)
    except json.JSONDecodeError:
        print(f"Error parsing '{config_file}'. Please ensure it's valid JSON.")
        raise

def _create_config_from_template(config_path: str, template_path: str) -> Dict[str, Any]:
    try:
        with open(template_path, 'r') as f:
            config = json.load(f)
        
        print("Please fill in the configuration values and save as 'qconfig.json'.")
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        return config
    except FileNotFoundError:
        print(f"Template file '{template_path}' not found. Please create a configuration file.")
        raise

def get_aws_session(profile: str = 'default') -> boto3.Session:
    config = load_config()
    return boto3.Session(profile_name=profile, region_name=config['region'])

def get_q_business_client(profile: str = 'default') -> boto3.client:
    session = get_aws_session(profile)
    return session.client('qbusiness')