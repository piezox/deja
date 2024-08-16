import boto3
import json

def load_config(config_file='qconfig.json', template_file='qconfig.template.json'):
    """
    Load the AWS Q configuration from a JSON file, falling back to a template if the main file doesn't exist.
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        if any(not value for value in config.values()):
            print(f"Warning: Some values in '{config_file}' are empty. Please fill them in.")
        
        return config
    except FileNotFoundError:
        try:
            with open(template_file, 'r') as f:
                config = json.load(f)
            
            print(f"Configuration file '{config_file}' not found. Using template '{template_file}'.")
            print("Please fill in the configuration values and save as 'qconfig.json'.")
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            return config
        except FileNotFoundError:
            print(f"Neither '{config_file}' nor '{template_file}' found. Please create a configuration file.")
            exit(1)
    except json.JSONDecodeError:
        print(f"Error parsing '{config_file}'. Please ensure it's valid JSON.")
        exit(1)

def get_aws_session(profile='default'):
    config = load_config()
    return boto3.Session(region_name=config['region'])

def get_q_business_client(profile='default'):
    session = get_aws_session(profile)
    return session.client('qbusiness')