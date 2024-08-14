# AWS Q CLI Uploader

This Python script provides a command-line interface for uploading files or adding URLs to AWS Q. It supports both local file uploads and adding URLs to existing web crawler data sources in AWS Q.

## Features

- Upload local files to AWS Q
- Add URLs to existing web crawler data sources in AWS Q
- Configuration management with template support
- Flexible command-line interface

## Prerequisites

- Python 3.6 or higher
- AWS account with Q access
- `boto3` library installed

## Installation

1. Clone this repository or download the script.

2. Install the required Python libraries:

   ```
   pip install boto3
   ```

3. Set up your AWS credentials. You can do this by:
   - Configuring the AWS CLI with `aws configure`
   - Setting environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
   - Using an AWS credentials file

## Configuration

1. Create a `qconfig.json` file in the same directory as the script with the following structure:

   ```json
   {
     "application_id": "your-application-id",
     "index_id": "your-index-id",
     "role_arn": "your-role-arn",
     "region": "your-aws-region"
   }
   ```

   Replace the placeholders with your actual AWS Q details.

2. Alternatively, you can create a `qconfig.template.json` file with empty values. The script will use this to create a `qconfig.json` file if it doesn't exist.

## Usage

### Uploading a local file

```
python aws_q_uploader.py path/to/your/file --crawler your-crawler-name
```

### Adding a URL to a web crawler

```
python aws_q_uploader.py https://example.com --crawler your-crawler-name
```

### Using a custom configuration file

```
python aws_q_uploader.py path/to/your/file --crawler your-crawler-name --config path/to/your/config.json
```

## Command-line Arguments

- `source`: The path to the local file or the URL to upload (required)
- `--crawler`: The name of the existing web crawler data source (required)
- `--config`: Path to the configuration file (optional, defaults to `qconfig.json`)

## Error Handling

The script includes error handling for common issues such as:
- Missing configuration files
- Invalid JSON in configuration files
- File not found errors
- AWS Q API errors

If you encounter any issues, check the error messages for guidance.

## Contributing

Contributions to improve the script are welcome. Please feel free to submit pull requests or open issues to discuss potential changes.

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]

## Disclaimer

This script is provided as-is, without any warranties. Always test thoroughly before using in a production environment.
