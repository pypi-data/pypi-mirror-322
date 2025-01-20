# Salesforce Spark Connector

A scalable Python connector for Salesforce that supports multiple data processing engines (Apache Spark, DuckDB) and various authentication methods.

## Environment Setup

1. Copy the template environment file:
```bash
cp .env.template .env
```

2. Update `.env` with your Salesforce credentials:
- For password authentication:
```
SF_USERNAME=your_username
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
```

- For OAuth authentication:
```
SF_CLIENT_ID=your_client_id
SF_CLIENT_SECRET=your_client_secret
```
Note: Other OAuth settings are pre-configured in the template

3. Never commit `.env` file with real credentials

## Features

- **Multiple Authentication Methods**:
  - OAuth2 with PKCE
  - JWT Bearer Flow
  - Certificate-based JWT
  - Username/Password
  - AWS Secrets Manager integration

- **Bulk API Support**:
  - Bulk API v2 for efficient data loading
  - Support for insert, update, delete operations
  - Automatic CSV handling and conversion
  - Configurable line endings and delimiters
  - Detailed job status monitoring and result tracking
  - Automatic ID mapping and status updates
  - Comprehensive error handling and reporting

- **Flexible Data Processing**:
  - Apache Spark support
  - DuckDB integration for efficient local processing
  - AWS Glue compatibility
  - Automatic format detection and conversion

 **Advanced Extraction Capabilities**
  - Parallel data extraction with automatic partitioning
  - Smart query partitioning based on field types
  - Automatic format conversion
  - Configurable number of partitions

- **Performance Optimizations**:
  - Efficient data pagination
  - Field type caching
  - Memory-efficient processing
  - Configurable batch sizes

- **Data Formats**:
  - Spark DataFrames
  - DuckDB Relations
  - AWS Glue DynamicFrames
  - Pandas DataFrames
  - Dictionary/JSON

## Installation

Basic installation:
```bash
pip install salesforce-spark-connector
```

With Spark support:
```bash
pip install "salesforce-spark-connector[spark]"
```

With development tools:
```bash
pip install "salesforce-spark-connector[dev]"
```

## Quick Start

### Basic Query
```python
from salesforce_connector import ScalableSalesforceConnector
from salesforce_connector.config import SalesforceConfig, AWSConfig, ProcessingConfig

# Configure the connector
sf_config = SalesforceConfig(
    auth_method='jwt_secret',
    client_id='your_client_id',
    username='your_username'
)

# Initialize connector
connector = ScalableSalesforceConnector(sf_config=sf_config)

# Extract data with automatic format detection
data = connector.extract_data("SELECT Id, Name FROM Account LIMIT 5")
```

### Bulk API v2 with Result Tracking
```python
from salesforce_connector import ScalableSalesforceConnector
from salesforce_connector.config import SalesforceConfig

# Configure connector
sf_config = SalesforceConfig(
    auth_method='password',
    username='your_username',
    password='your_password',
    security_token='your_token'
)

# Prepare data
accounts_to_insert = [
    {
        'Name': 'Test Account 1',
        'Industry': 'Technology',
        'Type': 'Customer'
    },
    {
        'Name': 'Test Account 2',
        'Industry': 'Healthcare',
        'Type': 'Customer'
    }
]

with ScalableSalesforceConnector(sf_config=sf_config) as connector:
    # Perform bulk insert with result tracking
    job_info = connector.bulk_v2_operation(
        object_name='Account',
        operation='insert',
        data=accounts_to_insert,
        wait=True,
        return_records=True  # Enable result tracking
    )

    # Process results
    if job_info['state'] == 'JobComplete':
        for record in job_info['records']:
            print(f"Account: {record['Name']}")
            print(f"Status: {record['status']}")
            if record['status'] == 'Success':
                print(f"Salesforce ID: {record['sf_id']}")
            else:
                print(f"Error: {record.get('error', 'Unknown error')}")
```

### Bulk API v2 Advanced Configuration
```python
# Configure bulk operation with specific settings
job_info = connector.bulk_v2_operation(
    object_name='Account',
    operation='insert',
    data=accounts_to_insert,
    line_ending="LF",        # Line ending type (LF or CRLF)
    column_delimiter="COMMA", # Column delimiter (COMMA, SEMICOLON, etc.)
    wait=True,               # Wait for job completion
    timeout=3600,           # Maximum time to wait (seconds)
    return_records=True     # Enable result tracking
)

# Job information includes:
# - state: Job state (JobComplete, Failed, etc.)
# - numberRecordsProcessed: Total records processed
# - numberRecordsFailed: Number of failed records
# - records: List of records with results (if return_records=True)
#   - Each record includes original data plus:
#   - sf_id: Salesforce ID (for successful records)
#   - status: Success/Failed/Unknown
#   - error: Error message (for failed records)
```

## Authentication Methods

### JWT Bearer Flow
```python
sf_config = SalesforceConfig(
    auth_method='jwt_secret',
    client_id='your_client_id'
)
aws_config = AWSConfig(
    secret_values={'auth_token': 'your_jwt_token'}
)
```

### OAuth2 with PKCE
```python
sf_config = SalesforceConfig(
    auth_method='oauth',
    client_id='your_client_id',
    client_secret='your_client_secret',
    redirect_uri='your_redirect_uri'
)
```

### Username/Password
```python
sf_config = SalesforceConfig(
    auth_method='password',
    username='your_username',
    password='your_password',
    security_token='your_security_token'
)
```

## Data Processing Examples

### Using DuckDB
```python
# Extract and analyze data
data = connector.extract_data("SELECT Id, Amount FROM Opportunity")
analysis = connector.query_data("""
    SELECT 
        DATE_TRUNC('month', CloseDate) as month,
        SUM(Amount) as total_amount
    FROM sf_data_latest
    GROUP BY 1
    ORDER BY 1
""")
```

### Using Spark
```python
proc_config = ProcessingConfig(require_spark=True)
connector = ScalableSalesforceConnector(
    sf_config=sf_config,
    processing_config=proc_config
)

# Get Spark DataFrame
spark_df = connector.extract_data(
    "SELECT Id, Name FROM Account",
    output_format='spark'
)

# Extract data with parallel processing
results = connector.extract_data(
    "SELECT Id, Name, CreatedDate FROM Account",
    partition_field="CreatedDate",
    num_partitions=5,
    output_format='spark'
)

```

### Using AWS Glue
```python
from awsglue.context import GlueContext
from pyspark.context import SparkContext

sc = SparkContext()
glue_context = GlueContext(sc)

proc_config = ProcessingConfig(glue_context=glue_context)
connector = ScalableSalesforceConnector(
    sf_config=sf_config,
    processing_config=proc_config
)

# Get DynamicFrame
dynamic_frame = connector.extract_data(
    "SELECT Id, Name FROM Account",
    output_format='dynamicframe'
)
```

## Configuration Options

### SalesforceConfig
- `auth_method`: Authentication method ('oauth', 'jwt', 'password')
- `client_id`: OAuth client ID
- `client_secret`: OAuth client secret (optional)
- `username`: Salesforce username (for password auth)
- `password`: Salesforce password (for password auth)
- `security_token`: Security token (for password auth)
- `domain`: Salesforce domain (default: 'login')
- `version`: API version (default: '54.0')

### ProcessingConfig
- `require_spark`: Enable Spark processing
- `require_duckdb`: Enable DuckDB support
- `spark_config`: Spark configuration options
- `duckdb_memory_limit`: DuckDB memory limit
- `cache_size`: Field metadata cache size

## Dependencies

- `simple-salesforce>=1.12.4`
- `requests-oauthlib>=1.3.1`
- `pyspark>=3.0.0` (optional)
- `duckdb>=0.9.0` (optional)
- `pandas>=1.3.0`
- `pyarrow>=14.0.1`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
