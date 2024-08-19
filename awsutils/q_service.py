import base64
import os
from .awsutils import get_q_business_client, load_config

class QService:
    def __init__(self, profile='default', region=None):
        self.config = load_config()
        self.client = get_q_business_client(profile, region)

    def upload_to_aws_q(self, source):
        with open(source, 'rb') as file:
            document_content = file.read()
            encoded_content = base64.b64encode(document_content).decode('utf-8')

        # Get file extension and map to content type
        _, file_extension = os.path.splitext(source)
        content_type = self.get_content_type(file_extension)

        document = {
            'id': os.path.basename(source),  # Use filename as id
            'title': os.path.basename(source),  # Use filename as title
            'content': {
                'blob': encoded_content
            },
            'contentType': content_type
        }

        try:
            response = self.client.batch_put_document(
                applicationId=self.config['application_id'],
                indexId=self.config['index_id'],
                documents=[document],
                roleArn=self.config['role_arn']
            )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f"Successfully uploaded: {source}")
            else:
                print(f"Failed to upload: {source}")
                print(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @staticmethod
    def get_content_type(file_extension):
        content_types = {
            '.pdf': 'PDF',
            '.html': 'HTML',
            '.htm': 'HTML',
            '.doc': 'MS_WORD',
            '.docx': 'MS_WORD',
            '.txt': 'PLAIN_TEXT',
            '.ppt': 'PPT',
            '.pptx': 'PPT',
            '.rtf': 'RTF',
            '.xml': 'XML',
            '.xsl': 'XSLT',
            '.xls': 'MS_EXCEL',
            '.xlsx': 'MS_EXCEL',
            '.csv': 'CSV',
            '.json': 'JSON',
            '.md': 'MD'
        }
        return content_types.get(file_extension.lower(), 'PLAIN_TEXT')

    def add_url_to_webcrawler(self, source, crawler_name):
        try:
            data_sources = self.client.list_data_sources(
                applicationId=self.config['application_id'],
                indexId=self.config['index_id'],
            )
            print(f"list_data_sources response: {data_sources}")

            existing_crawler = next((ds for ds in data_sources['type'] if ds['displayName'] == crawler_name), None)

            if existing_crawler:
                existing_seed_urls = [conn['SeedUrl'] for conn in existing_crawler['SeedUrlConnections']]
                existing_seed_urls.append(source)

                self.client.update_data_source(
                    applicationId=self.config['application_id'],
                    DataSourceId=existing_crawler['DataSourceId'],
                    indexId=self.config['index_id'],
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
