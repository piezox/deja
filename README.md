# DejaQ: AWS Q CLI Uploader

DejaQ is a Python package that provides a command-line interface for uploading files or adding URLs to AWS Q. It supports both local file uploads and adding URLs to existing web crawler data sources in AWS Q.

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

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/dejaq.git
   cd dejaq
   ```

2. Install the package:
   ```
   pip install -e .
   ```

   This will install DejaQ and its dependencies.

## Configuration

1. Create a `qconfig.json` file in the `awsutils` directory with the following structure:

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

You can use DejaQ either by running the Python module or by using the installed command-line tool.

### Using the Python module

```
python -m dejaq [source] [options]
```

### Using the command-line tool

```
dejaq [source] [options]
```

### Arguments and Options

- `source`: The URL or file path to upload (required)
- `--crawler`: Name of the existing web crawler data source (required for URLs)
- `--config`: Path to the configuration file (optional, defaults to 'qconfig.json')
- `--profile`: AWS profile to use (optional, defaults to 'default')

### Examples

1. Upload a file:
   ```
   dejaq /path/to/your/file.txt
   ```

2. Add a URL to a web crawler:
   ```
   dejaq https://example.com --crawler MyCrawler
   ```

3. Use a custom configuration file:
   ```
   dejaq /path/to/your/file.txt --config /path/to/custom/config.json
   ```

4. Use a specific AWS profile:
   ```
   dejaq /path/to/your/file.txt --profile my-aws-profile
   ```

## Using the run_dejaq.sh Script

For Unix-based systems, you can use the provided `run_dejaq.sh` script:

1. Make the script executable:
   ```
   chmod +x run_dejaq.sh
   ```

2. Run DejaQ using the script:
   ```
   ./run_dejaq.sh [source] [options]
   ```

This script will create and manage a virtual environment for you.

## Running Tests

To run the unit tests, use the following command from the project root directory:

```
python -m unittest discover tests
```

## Contributing

Contributions to improve DejaQ are welcome. Please feel free to submit pull requests or open issues to discuss potential changes.

## License

This project is released under the MIT License. See the LICENSE file for details.
