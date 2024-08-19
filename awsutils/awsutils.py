import os
import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound

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

def get_aws_session(profile='default', region=None):
    config = load_config()
    session_kwargs = {}

    if profile != 'default':
        session_kwargs['profile_name'] = profile

    if region:
        session_kwargs['region_name'] = region
    elif 'region' in config:
        session_kwargs['region_name'] = config['region']
    elif 'AWS_DEFAULT_REGION' in os.environ:
        session_kwargs['region_name'] = os.environ['AWS_DEFAULT_REGION']

    try:
        session = boto3.Session(**session_kwargs)
        # Test the session by making a simple API call
        session.client('sts').get_caller_identity()
        return session
    except NoCredentialsError:
        raise Exception("No AWS credentials found. Please configure your AWS credentials.")
    except ProfileNotFound:
        raise Exception(f"AWS profile '{profile}' not found. Please check your AWS configuration.")
    except ClientError as e:
        raise Exception(f"Error creating AWS session: {str(e)}")

def get_q_business_client(profile='default', region=None):
    try:
        session = get_aws_session(profile, region)
        return session.client('qbusiness')
    except Exception as e:
        raise Exception(f"Error creating Q Business client: {str(e)}")

def get_q_business_client(profile='default', region=None):
    session = get_aws_session(profile, region)
    try:
        return session.client('qbusiness')
    except ClientError as e:
        raise Exception(f"Error creating Q Business client: {str(e)}")