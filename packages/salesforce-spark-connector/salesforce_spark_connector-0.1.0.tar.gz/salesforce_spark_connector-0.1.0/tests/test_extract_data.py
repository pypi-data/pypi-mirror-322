from salesforce_connector import ScalableSalesforceConnector
from salesforce_connector.config import SalesforceConfig, AWSConfig, ProcessingConfig
import duckdb
from pyspark.sql import SparkSession
from typing import Optional, Dict, Any
from dataclasses import dataclass

def main():
    # Define your secret values
    print("starting main")
    secret_values = {
        "host": "https://login.salesforce.com",
        "username": "timmapuramreddy@example.com.sfdcdev",
        "auth_token": "<<JWT_TOKEN>>",
        "created_at": "2024-07-15T07:35:35",
        "expired_at": "2025-07-15T07:35:35"
    }
    # Example usage
    spark_config = {
    "spark.executor.memory": "2g",
    "spark.driver.memory": "1g"
    }

    # spark_session = create_spark_session(spark_config)
    # spark_context = spark_session.sparkContext

    # Create configuration instances
    sf_config = SalesforceConfig(
        auth_method='jwt_secret',
        version='54.0'
    )
    aws_config = AWSConfig(
        secret_values=secret_values
    )
    proc_config = ProcessingConfig(
        spark_config=spark_config,
        require_spark=True,
        require_duckdb=True
    )
    # Create an instance of ScalableSalesforceConnector
    connector = ScalableSalesforceConnector(
        sf_config=sf_config,
        aws_config=aws_config,
        processing_config=proc_config,
        log_level='DEBUG'
    )

    try:
        # Use the extract_data method
        query = "SELECT Id, Amount, CreatedDate FROM Opportunity where Amount<600 and Amount>100"
        data = connector.extract_data(query=query, output_format='duckdb', partition_field="Amount", num_partitions=5)
        
        # Display the results using DuckDB
        if isinstance(data, duckdb.DuckDBPyRelation):
            data.show()
        else:
            print("Unexpected data format:", type(data))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure resources are cleaned up
        connector.close()


if __name__ == "__main__":
    main()