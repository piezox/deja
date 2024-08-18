import argparse
from urllib.parse import urlparse
from typing import Optional
from awsutils.q_service import QService

def is_url(path: str) -> bool:
    """Check if the given path is a valid URL."""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def process_source(q_service: QService, source: str, crawler_name: Optional[str]) -> None:
    """Process the source based on whether it's a URL or a file."""
    if is_url(source):
        if not crawler_name:
            raise ValueError("Crawler name is required for URL sources.")
        q_service.add_url_to_webcrawler(source, crawler_name)
    else:
        q_service.upload_to_aws_q(source)

def main() -> None:
    parser = argparse.ArgumentParser(description='Upload a URL or file to AWS Q')
    parser.add_argument('source', help='URL or file path to upload')
    parser.add_argument('--crawler', help='Name of the existing web crawler data source')
    parser.add_argument('--config', default='qconfig.json', help='Path to the configuration file')
    parser.add_argument('--profile', default='default', help='AWS profile to use')

    args = parser.parse_args()

    try:
        q_service = QService(args.profile, config_file=args.config)
        process_source(q_service, args.source, args.crawler)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()