from typing import Dict, List, Optional, Union
import json
import time
import requests
import logging
from ..utils.logging_utils import setup_logging

class BulkV2Operations:
    def __init__(self, sf, logger=None):
        """
        Initialize Bulk API v2 operations handler.
        
        Args:
            sf: Salesforce connection instance
            logger: Logger instance (optional)
        """
        self.sf = sf
        self.logger = logger or setup_logging()
        
        try:
            # Get API version from Salesforce instance
            version_str = getattr(self.sf, 'api_version', '57.0')
            self.api_version = float(str(version_str).replace('v', ''))
        except (ValueError, AttributeError) as e:
            self.logger.warning(f"Failed to parse version number: {e}")
            self.api_version = 57.0
        
        # Get instance URL from Salesforce connection
        try:
            # Try different ways to get instance URL based on auth method
            if hasattr(self.sf, 'sf_instance'):
                instance_url = f"https://{self.sf.sf_instance}"
            elif hasattr(self.sf, 'instance_url'):
                instance_url = self.sf.instance_url
            else:
                # Fallback to constructing from session
                instance_url = f"https://{self.sf.session.server}"
                
            if not instance_url.startswith('http'):
                instance_url = f"https://{instance_url}"
                
            self.base_url = f"{instance_url}/services/data/v{self.api_version}/jobs/ingest"
            self.logger.debug(f"Bulk API V2 base URL: {self.base_url}")
            
        except Exception as e:
            self.logger.error(f"Failed to construct Bulk API V2 URL: {e}")
            raise

    def _get_auth_header(self):
        """
        Get appropriate authorization header based on authentication method
        """
        try:
            # Try to get session id directly first (password auth)
            if hasattr(self.sf, 'session_id'):
                return f'OAuth {self.sf.session_id}'
            # Try OAuth token next
            elif hasattr(self.sf.session, 'auth') and hasattr(self.sf.session.auth, 'access_token'):
                return f'OAuth {self.sf.session.auth.access_token}'
            # Finally try session headers
            elif hasattr(self.sf, 'headers') and 'Authorization' in self.sf.headers:
                return self.sf.headers['Authorization']
            else:
                raise ValueError("Could not find valid authentication token")
        except Exception as e:
            self.logger.error(f"Failed to get authorization header: {e}")
            raise

    def create_job(self, object_name: str, operation: str, 
                  line_ending: str = "LF", 
                  column_delimiter: str = "COMMA") -> Dict:
        """
        Create a Bulk API v2 job.
        
        Args:
            object_name: Salesforce object name
            operation: Operation type (insert, update, delete, upsert)
            line_ending: Line ending type (LF recommended, CRLF supported)
            column_delimiter: Column delimiter (COMMA, SEMICOLON, PIPE, TAB)
        """
        # Get headers with proper authentication
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json',
            'Authorization': self._get_auth_header()
        }
        
        payload = {
            "object": object_name,
            "contentType": "CSV",
            "operation": operation,
            "lineEnding": line_ending,
            "columnDelimiter": column_delimiter
        }
        
        self.logger.debug(f"Creating Bulk API V2 job for {object_name} with operation {operation}")
        
        response = requests.post(
            self.base_url,
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code >= 400:
            self.logger.error(f"Failed to create job: {response.text}")
            response.raise_for_status()
            
        return response.json()

    def upload_job_data(self, job_id: str, data: Union[str, List[Dict]], line_ending: str = "LF") -> None:
        """
        Upload data for a Bulk API v2 job.
        
        Args:
            job_id: Job ID from create_job
            data: CSV string or list of dictionaries to upload
            line_ending: Line ending to use (LF or CRLF)
        """
        headers = {
            'Content-Type': 'text/csv',
            'Accept': 'application/json',
            'Authorization': self._get_auth_header()
        }
        
        # Convert dict list to CSV if needed
        if isinstance(data, list):
            import csv
            import io
            output = io.StringIO(newline='')  # Important: let csv module handle line endings
            if data:
                # Ensure all required fields are present
                fieldnames = set()
                for record in data:
                    fieldnames.update(record.keys())
                
                writer = csv.DictWriter(
                    output, 
                    fieldnames=sorted(fieldnames),
                    lineterminator='\n' if line_ending == "LF" else '\r\n'
                )
                writer.writeheader()
                writer.writerows(data)
                data = output.getvalue()
                
                self.logger.debug(f"CSV Data to upload: {data}")
        
        self.logger.debug(f"Uploading data to job {job_id}")
        
        # Ensure consistent line endings in the final data
        if isinstance(data, str):
            if line_ending == "LF":
                data = data.replace('\r\n', '\n')
            else:  # CRLF
                data = data.replace('\n', '\r\n')
        
        response = requests.put(
            f"{self.base_url}/{job_id}/batches",
            headers=headers,
            data=data.encode('utf-8')
        )
        
        if response.status_code >= 400:
            self.logger.error(f"Failed to upload data: {response.text}")
            response.raise_for_status()

    def close_job(self, job_id: str) -> Dict:
        """
        Close a Bulk API v2 job for processing.
        
        Args:
            job_id: Job ID to close
            
        Returns:
            Job status information
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self._get_auth_header()
        }
        
        payload = {"state": "UploadComplete"}
        
        response = requests.patch(
            f"{self.base_url}/{job_id}",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code >= 400:
            self.logger.error(f"Failed to close job: {response.text}")
            response.raise_for_status()
            
        return response.json()

    def get_job_status(self, job_id: str) -> Dict:
        """
        Get the status of a Bulk API v2 job.
        
        Args:
            job_id: Job ID to check
            
        Returns:
            Job status information
        """
        response = requests.get(
            f"{self.base_url}/{job_id}",
            headers=self.sf.headers
        )
        
        if response.status_code >= 400:
            self.logger.error(f"Failed to get job status: {response.text}")
            response.raise_for_status()
            
        return response.json()

    def get_job_results(self, job_id: str, include_success: bool = True) -> str:
        """
        Get the results of a completed Bulk API v2 job.
        
        Args:
            job_id: Job ID to get results for
            include_success: Whether to include successful records
            
        Returns:
            CSV string of results
        """
        result_type = "successfulResults" if include_success else "failedResults"
        
        response = requests.get(
            f"{self.base_url}/{job_id}/{result_type}",
            headers=self.sf.headers
        )
        
        if response.status_code >= 400:
            self.logger.error(f"Failed to get job results: {response.text}")
            response.raise_for_status()
            
        return response.text

    def wait_for_job(self, job_id: str, timeout: int = 3600, 
                     check_interval: int = 10) -> Dict:
        """
        Wait for a job to complete.
        
        Args:
            job_id: Job ID to wait for
            timeout: Maximum time to wait in seconds
            check_interval: Time between status checks in seconds
            
        Returns:
            Final job status
        """
        start_time = time.time()
        while True:
            status = self.get_job_status(job_id)
            
            if status['state'] in ['JobComplete', 'Failed', 'Aborted']:
                return status
                
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")
                
            time.sleep(check_interval) 

    def get_job_details(self, job_id: str) -> Dict:
        """
        Get detailed information about a job, including any error messages.
        """
        headers = {
            'Accept': 'application/json',
            'Authorization': self._get_auth_header()
        }
        
        response = requests.get(
            f"{self.base_url}/{job_id}",
            headers=headers
        )
        
        if response.status_code >= 400:
            self.logger.error(f"Failed to get job details: {response.text}")
            response.raise_for_status()
        
        job_info = response.json()
        if job_info['state'] == 'Failed':
            self.logger.error(f"Job failed: {job_info.get('errorMessage', 'No error message available')}")
            if 'errors' in job_info:
                for error in job_info['errors']:
                    self.logger.error(f"Error details: {error}")
        
        return job_info 

    def get_job_results_with_mapping(self, job_id: str, data: List[Dict]) -> List[Dict]:
        """
        Get job results and map them back to the input records.
        
        Args:
            job_id: Job ID to get results for
            data: Original input records
            
        Returns:
            List of input records enriched with Salesforce IDs and status
        """
        # Get successful and failed results
        success_results = self.get_job_results(job_id, True)
        failed_results = self.get_job_results(job_id, False)
        
        # Parse CSV results
        import csv
        from io import StringIO
        
        success_records = list(csv.DictReader(StringIO(success_results))) if success_results else []
        failed_records = list(csv.DictReader(StringIO(failed_results))) if failed_results else []
        
        # Log raw results for debugging
        self.logger.debug(f"Success records: {success_records}")
        self.logger.debug(f"Failed records: {failed_records}")
        
        # Create enriched records with results
        enriched_records = []
        for record in data:
            record_copy = record.copy()
            name = record['Name']
            
            # Find corresponding result record
            success_record = next((r for r in success_records if r['Name'] == name), None)
            failed_record = next((r for r in failed_records if r['Name'] == name), None)
            
            if success_record:
                # Record was successful
                record_copy.update({
                    'sf_id': success_record['sf__Id'],
                    'status': 'Success'
                })
            elif failed_record:
                # Record failed
                record_copy.update({
                    'error': failed_record.get('sf__Error', 'Unknown error'),
                    'status': 'Failed'
                })
            else:
                # Record not found in results
                record_copy['status'] = 'Unknown'
            
            enriched_records.append(record_copy)
            self.logger.debug(f"Enriched record: {record_copy}")
        
        return enriched_records 