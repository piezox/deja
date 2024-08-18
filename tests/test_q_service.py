import unittest
from unittest.mock import patch, MagicMock
from awsutils.q_service import QService

class TestQService(unittest.TestCase):

    @patch('awsutils.q_service.get_q_business_client')
    @patch('awsutils.q_service.load_config')
    def setUp(self, mock_load_config, mock_get_q_business_client):
        self.mock_config = {
            'application_id': 'test-app-id',
            'index_id': 'test-index-id',
            'role_arn': 'test-role-arn',
            'region': 'us-west-2'
        }
        mock_load_config.return_value = self.mock_config
        self.mock_client = MagicMock()
        mock_get_q_business_client.return_value = self.mock_client
        self.q_service = QService()

    def test_init(self):
        self.assertEqual(self.q_service.config, self.mock_config)
        self.assertEqual(self.q_service.client, self.mock_client)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b'test content')
    def test_upload_to_aws_q_success(self, mock_open):
        self.mock_client.batch_put_document.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        
        self.q_service.upload_to_aws_q('test_file.txt')
        
        self.mock_client.batch_put_document.assert_called_once_with(
            applicationId='test-app-id',
            indexId='test-index-id',
            documents=[{
                'id': 'id',
                'title': 'title',
                'content': {
                    'blob': b'test content'
                }
            }],
            roleArn='test-role-arn'
        )

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b'test content')
    def test_upload_to_aws_q_failure(self, mock_open):
        self.mock_client.batch_put_document.return_value = {'ResponseMetadata': {'HTTPStatusCode': 400}}
        
        with self.assertRaises(Exception):
            self.q_service.upload_to_aws_q('test_file.txt')

    def test_add_url_to_webcrawler_success(self):
        self.mock_client.list_data_sources.return_value = {
            'type': [{
                'displayName': 'test_crawler',
                'DataSourceId': 'test-ds-id',
                'SeedUrlConnections': [{'SeedUrl': 'http://example.com'}],
                'Authentication': {}
            }]
        }
        
        self.q_service.add_url_to_webcrawler('http://newexample.com', 'test_crawler')
        
        self.mock_client.update_data_source.assert_called_once_with(
            applicationId='test-app-id',
            DataSourceId='test-ds-id',
            indexId='test-index-id',
            Configuration={
                'Name': 'test_crawler',
                'SeedUrlConnections': [
                    {'SeedUrl': 'http://example.com'},
                    {'SeedUrl': 'http://newexample.com'}
                ],
                'Authentication': {}
            }
        )

    def test_add_url_to_webcrawler_crawler_not_found(self):
        self.mock_client.list_data_sources.return_value = {'type': []}
        
        with self.assertRaises(Exception):
            self.q_service.add_url_to_webcrawler('http://newexample.com', 'nonexistent_crawler')

if __name__ == '__main__':
    unittest.main()