import argparse
import logging
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound

from awsutils.q_service import QService

def is_url(path: str) -> bool:
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_file(q_service: QService, file_path: str) -> None:
    if not Path(file_path).is_file():
        raise ValueError(f"File not found: {file_path}")
    q_service.upload_to_aws_q(file_path)

def add_url(q_service: QService, url: str, crawler_name: Optional[str]) -> None:
    if not crawler_name:
        raise ValueError("Crawler name is required for adding URLs")
    q_service.add_url_to_webcrawler(url, crawler_name)

def main() -> None:
    parser = argparse.ArgumentParser(description='Upload a URL or file to AWS Q')
    parser.add_argument('source', help='URL or file path to upload')
    parser.add_argument('--crawler', required=False, help='Name of the existing web crawler data source')
    parser.add_argument('--config', default='qconfig.json', help='Path to the configuration file')
    parser.add_argument('--profile', default='default', help='AWS profile to use')
    parser.add_argument('--region', help='AWS region to use')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()
    setup_logging(args.verbose)

    try:
        q_service = QService(args.profile, args.region)

        if is_url(args.source):
            add_url(q_service, args.source, args.crawler)
        else:
            upload_file(q_service, args.source)

    except NoCredentialsError:
        logging.error("No AWS credentials found. Please configure your AWS credentials.")
    except ProfileNotFound:
        logging.error(f"AWS profile '{args.profile}' not found. Please check your AWS configuration.")
    except ClientError as e:
        logging.error(f"AWS client error: {str(e)}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()