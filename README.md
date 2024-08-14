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

This project is released under the MIT License:

```
MIT License

Copyright (c) 2024 Stefano Marzani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

This MIT License allows for unrestricted reuse and modification of this code by any developer, including for commercial purposes, provided that the above copyright notice and permission notice are included in all copies or substantial portions of the Software.

## Disclaimer

This script is provided as-is, without any warranties. Always test thoroughly before using in a production environment.
