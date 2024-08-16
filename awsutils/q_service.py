from .awsutils import get_q_business_client, load_config

class QService:
    def __init__(self, profile='default'):
        self.config = load_config()
        self.client = get_q_business_client(profile)

    def upload_to_aws_q(self, source):
        with open(source, 'rb') as file:
            document_content = file.read()

        document = {
            'id': "id",
            'title': "title",
            'content': {
                'blob': document_content
            }
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