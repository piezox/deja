import argparse
import boto3
import json
from urllib.parse import urlparse

def load_config(config_file='qconfig.json', template_file='qconfig.template.json'):
    """
    Load the AWS Q configuration from a JSON file, falling back to a template if the main file doesn't exist.
    
    :param config_file: Path to the main configuration file
    :param template_file: Path to the template configuration file
    :return: Dictionary containing the configuration
    """
    try:
        # Try to load the main configuration file
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Check if any required fields are empty
        if any(not value for value in config.values()):
            print(f"Warning: Some values in '{config_file}' are empty. Please fill them in.")
        
        return config
    except FileNotFoundError:
        # If the main config file is not found, try to load the template
        try:
            with open(template_file, 'r') as f:
                config = json.load(f)
            
            print(f"Configuration file '{config_file}' not found. Using template '{template_file}'.")
            print("Please fill in the configuration values and save as 'qconfig.json'.")
            
            # Create the main config file from the template
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            return config
        except FileNotFoundError:
            print(f"Neither '{config_file}' nor '{template_file}' found. Please create a configuration file.")
            exit(1)
    except json.JSONDecodeError:
        print(f"Error parsing '{config_file}'. Please ensure it's valid JSON.")
        exit(1)

def upload_to_aws_q(source, config):
    """
    Upload a file or URL content to AWS Q.
    
    :param source: Path to local file or URL to upload
    :param config: Dictionary containing AWS Q configuration
    """
    # Initialize AWS Q client
    q_business = boto3.client('qbusiness', region_name=config['region'])

    # Open the file in binary mode
    with open(source, 'rb') as file:
        # Read the file contents
        document_content = file.read()

        # Create a dictionary with the required keys
        document = {
            'id': "id",  # You can use a custom document ID if desired
            'title': "title",  # You can use a custom document title if desired
            'content': {
                'blob': document_content
            }
        }

        try:
            # Attempt to upload document to AWS Q
            response = q_business.batch_put_document(
                applicationId=config['application_id'],
                indexId=config['index_id'],
                documents=[document],
                roleArn=config['role_arn']
            )

            # Check upload status and print result
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f"Successfully uploaded: {source}")
            else:
                print(f"Failed to upload: {source}")
                print(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def is_url(path):
    """
    Check if the given path is a valid URL.
    
    :param path: String to check
    :return: True if path is a valid URL, False otherwise
    """
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def add_url_to_webcrawler(source, crawler_name, config):
    """
    Add a URL to an existing web crawler data source in AWS Q.

    :param source: URL to add as a seed URL
    :param crawler_name: Name of the existing web crawler data source
    :param config: Dictionary containing AWS Q configuration
    """
    # Initialize AWS Q client
    q_business = boto3.client('qbusiness', region_name=config['region'])

    try:
        # Get the existing web crawler data source
        data_sources = q_business.list_data_sources(
            applicationId=config['application_id'],
            indexId=config['index_id'],
        )
        print(f"list_data_sources response: {data_sources}")

        existing_crawler = next((ds for ds in data_sources['type'] if ds['displayName'] == crawler_name), None)

        if existing_crawler:
            # Add the new URL to the existing seed URLs
            existing_seed_urls = [conn['SeedUrl'] for conn in existing_crawler['SeedUrlConnections']]
            existing_seed_urls.append(source)

            # Update the web crawler data source with the new seed URLs
            q_business.update_data_source(
                applicationId=config['application_id'],
                DataSourceId=existing_crawler['DataSourceId'],
                indexId=config['index_id'],
                Configuration={
                    'Name': crawler_name,
                    'SeedUrlConnections': [{'SeedUrl': url} for url in existing_seed_urls],
                    'Authentication': existing_crawler['Authentication']
                }
            )

            print(f"Successfully added URL '{source}' to web crawler '{crawler_name}'")
        else:
            print(f"Web crawler '{crawler_name}' not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    """
    Main function to handle command-line arguments and initiate upload process.
    """

    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Upload a URL or file to AWS Q')
    parser.add_argument('source', help='URL or file path to upload')
    parser.add_argument('--crawler', required=True, help='Name of the existing web crawler data source')
    parser.add_argument('--config', default='qconfig.json', help='Path to the configuration file')

    # Parse command-line arguments
    args = parser.parse_args()

    # Parse command-line arguments
    args = parser.parse_args()

    # Load configuration from file
    config = load_config(args.config)

    # Determine if source is URL or local file and prepare content
    if is_url(args.source):
        # Handle URL: fetch content and use URL basename or full URL as title
        add_url_to_webcrawler(args.source, args.crawler, config)
    else:
        # Handle local file: read file content and use filename as title
        upload_to_aws_q(args.source, config)

if __name__ == "__main__":
    main()