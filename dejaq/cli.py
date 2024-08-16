import argparse
from urllib.parse import urlparse
from awsutils.q_service import QService

def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def main():
    parser = argparse.ArgumentParser(description='Upload a URL or file to AWS Q')
    parser.add_argument('source', help='URL or file path to upload')
    parser.add_argument('--crawler', required=False, help='Name of the existing web crawler data source')
    parser.add_argument('--config', default='qconfig.json', help='Path to the configuration file')
    parser.add_argument('--profile', default='default', help='AWS profile to use')

    args = parser.parse_args()

    q_service = QService(args.profile)

    if is_url(args.source):
        q_service.add_url_to_webcrawler(args.source, args.crawler)
    else:
        q_service.upload_to_aws_q(args.source)

if __name__ == "__main__":
    main()