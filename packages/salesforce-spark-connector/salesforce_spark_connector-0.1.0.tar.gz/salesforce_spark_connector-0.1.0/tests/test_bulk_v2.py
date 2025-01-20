import os
import unittest
import json
import time
from salesforce_connector.connector import ScalableSalesforceConnector
from salesforce_connector.config import ProcessingConfig
from salesforce_connector.utils.logging_utils import setup_logging
from tests.utils.env_loader import load_env, get_password_auth_config, get_oauth_config

# Load environment variables
load_env()

class TestBulkV2Operations(unittest.TestCase):
    def setUp(self):
        """Common setup for all tests"""
        self.logger = setup_logging(log_level='DEBUG')

    def test_bulk_insert_with_password_auth(self):
        """Test bulk insert using password authentication"""
        sf_config = get_password_auth_config()
        
        with ScalableSalesforceConnector(sf_config=sf_config, log_level='DEBUG') as connector:
            self._run_bulk_insert_test(connector)

    def test_bulk_insert_with_oauth(self):
        """Test bulk insert using OAuth PKCE authentication"""
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        sf_config = get_oauth_config()
        proc_config = ProcessingConfig(
            require_spark=False,
            require_duckdb=False
        )
        
        with ScalableSalesforceConnector(
            sf_config=sf_config, 
            processing_config=proc_config, 
            log_level='DEBUG'
        ) as connector:
            self._run_bulk_insert_test(connector)

    def test_bulk_insert_with_jwt_cert(self):
        """Test bulk insert using JWT certificate authentication"""
        # Use the same JWT config from test_jwt_auth.py
        from tests.test_jwt_auth import TEST_JWT_CONFIG
        
        with ScalableSalesforceConnector(sf_config=TEST_JWT_CONFIG, log_level='DEBUG') as connector:
            self._run_bulk_insert_test(connector)

    def test_bulk_insert_with_record_tracking(self):
        """Test bulk insert with record tracking enabled"""
        sf_config = get_password_auth_config()
        
        with ScalableSalesforceConnector(sf_config=sf_config, log_level='DEBUG') as connector:
            # Use timestamp to ensure unique names
            timestamp = int(time.time())
            test_accounts = [
                {
                    'Name': f'Bulk API Test Account {timestamp}_1',
                    'Industry': 'Technology',
                    'Type': 'Customer'
                },
                {
                    'Name': f'Bulk API Test Account {timestamp}_2',
                    'Industry': 'Healthcare',
                    'Type': 'Customer'
                }
            ]

            try:
                # Perform bulk insert with record tracking
                job_info = connector.bulk_v2_operation(
                    object_name='Account',
                    data=test_accounts,
                    operation='insert',
                    wait=True,
                    line_ending="LF",
                    return_records=True  # Enable record tracking
                )

                # Get detailed job info for debugging
                if hasattr(connector.bulk_v2, 'get_job_details'):
                    detailed_info = connector.bulk_v2.get_job_details(job_info['id'])
                    connector.logger.info(f"Detailed Job Info: {json.dumps(detailed_info, indent=2)}")

                # Verify job completed successfully
                self.assertEqual(
                    job_info['state'],
                    'JobComplete',
                    f"Job failed with state {job_info['state']}. Full job info: {json.dumps(job_info, indent=2)}"
                )

                # Verify record tracking results
                self.assertIn('records', job_info, "Record tracking results not found in job info")
                self.assertEqual(
                    len(job_info['records']),
                    len(test_accounts),
                    "Number of returned records doesn't match input"
                )

                # Verify each record
                for i, record in enumerate(job_info['records']):
                    # Verify original data is preserved
                    self.assertEqual(
                        record['Name'],
                        test_accounts[i]['Name'],
                        "Original record data not preserved"
                    )
                    self.assertEqual(
                        record['Industry'],
                        test_accounts[i]['Industry'],
                        "Original record data not preserved"
                    )

                    # Verify success status and Salesforce ID
                    self.assertEqual(
                        record['status'],
                        'Success',
                        f"Record {record['Name']} failed: {record.get('error', 'No error message')}"
                    )
                    self.assertIn('sf_id', record, f"Salesforce ID not found for record: {record['Name']}")
                    self.assertTrue(
                        record['sf_id'].startswith('001'),
                        f"Invalid Salesforce ID format: {record['sf_id']}"
                    )

                # Clean up test data
                for record in job_info['records']:
                    if record['status'] == 'Success':
                        try:
                            connector.sf.Account.delete(record['sf_id'])
                            connector.logger.debug(f"Deleted test account: {record['sf_id']}")
                        except Exception as e:
                            connector.logger.warning(f"Failed to delete test account {record['sf_id']}: {str(e)}")

            except Exception as e:
                connector.logger.error(f"Test failed with error: {str(e)}")
                raise

    def test_bulk_insert_with_failed_records(self):
        """Test bulk insert with some invalid records to test error handling"""
        sf_config = get_password_auth_config()
        
        with ScalableSalesforceConnector(sf_config=sf_config, log_level='DEBUG') as connector:
            timestamp = int(time.time())
            test_accounts = [
                {
                    'Name': f'Bulk API Test Account {timestamp}_1',
                    'Industry': 'Technology',
                    'Type': 'Customer'
                },
                {
                    'Name': '',  # Invalid: Name is required
                    'Industry': 'Healthcare',
                    'Type': 'Customer'
                }
            ]

            try:
                job_info = connector.bulk_v2_operation(
                    object_name='Account',
                    data=test_accounts,
                    operation='insert',
                    wait=True,
                    line_ending="LF",
                    return_records=True
                )

                # Verify mixed results
                self.assertEqual(
                    job_info['state'],
                    'JobComplete',
                    f"Job failed with unexpected state: {job_info['state']}"
                )

                success_count = len([r for r in job_info['records'] if r['status'] == 'Success'])
                failed_count = len([r for r in job_info['records'] if r['status'] == 'Failed'])

                self.assertEqual(success_count, 1, "Expected exactly one successful record")
                self.assertEqual(failed_count, 1, "Expected exactly one failed record")

                # Verify error message for failed record
                failed_record = next(r for r in job_info['records'] if r['status'] == 'Failed')
                self.assertIn('error', failed_record, "Error message not found in failed record")

                # Clean up successful records
                for record in job_info['records']:
                    if record['status'] == 'Success':
                        try:
                            connector.sf.Account.delete(record['sf_id'])
                        except Exception as e:
                            connector.logger.warning(f"Failed to delete test account {record['sf_id']}: {str(e)}")

            except Exception as e:
                connector.logger.error(f"Test failed with error: {str(e)}")
                raise

    def test_bulk_insert_with_record_tracking_oauth(self):
        """Test bulk insert with record tracking enabled using OAuth PKCE"""
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        sf_config = get_oauth_config()
        proc_config = ProcessingConfig(
            require_spark=False,
            require_duckdb=False
        )
        
        with ScalableSalesforceConnector(
            sf_config=sf_config, 
            processing_config=proc_config, 
            log_level='DEBUG'
        ) as connector:
            # Use timestamp to ensure unique names
            timestamp = int(time.time())
            test_accounts = [
                {
                    'Name': f'Bulk API OAuth Test Account {timestamp}_1',
                    'Industry': 'Technology',
                    'Type': 'Customer'
                },
                {
                    'Name': f'Bulk API OAuth Test Account {timestamp}_2',
                    'Industry': 'Healthcare',
                    'Type': 'Customer'
                }
            ]

            try:
                # Perform bulk insert with record tracking
                job_info = connector.bulk_v2_operation(
                    object_name='Account',
                    data=test_accounts,
                    operation='insert',
                    wait=True,
                    line_ending="LF",
                    return_records=True  # Enable record tracking
                )

                # Get detailed job info for debugging
                if hasattr(connector.bulk_v2, 'get_job_details'):
                    detailed_info = connector.bulk_v2.get_job_details(job_info['id'])
                    connector.logger.info(f"Detailed Job Info: {json.dumps(detailed_info, indent=2)}")

                # Verify job completed successfully
                self.assertEqual(
                    job_info['state'],
                    'JobComplete',
                    f"Job failed with state {job_info['state']}. Full job info: {json.dumps(job_info, indent=2)}"
                )

                # Verify record tracking results
                self.assertIn('records', job_info, "Record tracking results not found in job info")
                self.assertEqual(
                    len(job_info['records']),
                    len(test_accounts),
                    "Number of returned records doesn't match input"
                )

                # Verify each record
                for i, record in enumerate(job_info['records']):
                    # Verify original data is preserved
                    self.assertEqual(
                        record['Name'],
                        test_accounts[i]['Name'],
                        "Original record data not preserved"
                    )
                    self.assertEqual(
                        record['Industry'],
                        test_accounts[i]['Industry'],
                        "Original record data not preserved"
                    )

                    # Verify success status and Salesforce ID
                    self.assertEqual(
                        record['status'],
                        'Success',
                        f"Record {record['Name']} failed: {record.get('error', 'No error message')}"
                    )
                    self.assertIn('sf_id', record, f"Salesforce ID not found for record: {record['Name']}")
                    self.assertTrue(
                        record['sf_id'].startswith('001'),
                        f"Invalid Salesforce ID format: {record['sf_id']}"
                    )

                # Clean up test data
                for record in job_info['records']:
                    if record['status'] == 'Success':
                        try:
                            connector.sf.Account.delete(record['sf_id'])
                            connector.logger.debug(f"Deleted test account: {record['sf_id']}")
                        except Exception as e:
                            connector.logger.warning(f"Failed to delete test account {record['sf_id']}: {str(e)}")

            except Exception as e:
                connector.logger.error(f"Test failed with error: {str(e)}")
                raise

    def test_bulk_insert_with_failed_records_oauth(self):
        """Test bulk insert with some invalid records using OAuth PKCE"""
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        sf_config = get_oauth_config()
        proc_config = ProcessingConfig(
            require_spark=False,
            require_duckdb=False
        )
        
        with ScalableSalesforceConnector(
            sf_config=sf_config, 
            processing_config=proc_config, 
            log_level='DEBUG'
        ) as connector:
            timestamp = int(time.time())
            test_accounts = [
                {
                    'Name': f'Bulk API OAuth Test Account {timestamp}_1',
                    'Industry': 'Technology',
                    'Type': 'Customer'
                },
                {
                    'Name': '',  # Invalid: Name is required
                    'Industry': 'Healthcare',
                    'Type': 'Customer'
                }
            ]

            try:
                job_info = connector.bulk_v2_operation(
                    object_name='Account',
                    data=test_accounts,
                    operation='insert',
                    wait=True,
                    line_ending="LF",
                    return_records=True
                )

                # Verify mixed results
                self.assertEqual(
                    job_info['state'],
                    'JobComplete',
                    f"Job failed with unexpected state: {job_info['state']}"
                )

                success_count = len([r for r in job_info['records'] if r['status'] == 'Success'])
                failed_count = len([r for r in job_info['records'] if r['status'] == 'Failed'])

                self.assertEqual(success_count, 1, "Expected exactly one successful record")
                self.assertEqual(failed_count, 1, "Expected exactly one failed record")

                # Verify error message for failed record
                failed_record = next(r for r in job_info['records'] if r['status'] == 'Failed')
                self.assertIn('error', failed_record, "Error message not found in failed record")

                # Clean up successful records
                for record in job_info['records']:
                    if record['status'] == 'Success':
                        try:
                            connector.sf.Account.delete(record['sf_id'])
                        except Exception as e:
                            connector.logger.warning(f"Failed to delete test account {record['sf_id']}: {str(e)}")

            except Exception as e:
                connector.logger.error(f"Test failed with error: {str(e)}")
                raise

    def _run_bulk_insert_test(self, connector):
        """Common test logic for bulk insert across different auth methods"""
        # Use timestamp to ensure unique names
        timestamp = int(time.time())
        test_accounts = [
            {
                'Name': f'Bulk API Test Account {timestamp}_1',
                'Industry': 'Technology',
                'Type': 'Customer'
            },
            {
                'Name': f'Bulk API Test Account {timestamp}_2',
                'Industry': 'Healthcare',
                'Type': 'Customer'
            }
        ]

        try:
            job_info = connector.bulk_v2_operation(
                object_name='Account',
                data=test_accounts,
                operation='insert',
                wait=True,
                line_ending="LF"
            )

            # Get detailed job info for debugging
            if hasattr(connector.bulk_v2, 'get_job_details'):
                detailed_info = connector.bulk_v2.get_job_details(job_info['id'])
                connector.logger.info(f"Detailed Job Info: {json.dumps(detailed_info, indent=2)}")

            # Assertions
            self.assertIn(
                job_info['state'], 
                ['JobComplete', 'InProgress'],
                f"Job failed with state {job_info['state']}. Full job info: {json.dumps(job_info, indent=2)}"
            )
            
            if job_info['state'] == 'JobComplete':
                self.assertEqual(
                    job_info['numberRecordsFailed'], 
                    0, 
                    f"Some records failed to insert. Job info: {json.dumps(job_info, indent=2)}"
                )
                self.assertEqual(
                    job_info['numberRecordsProcessed'],
                    2,
                    f"Not all records were processed. Job info: {json.dumps(job_info, indent=2)}"
                )

        except Exception as e:
            connector.logger.error(f"Test failed with error: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main() 