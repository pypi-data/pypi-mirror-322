# tests/test_oauth_pkce_auth.py
import os
from salesforce_connector import ScalableSalesforceConnector
from salesforce_connector.config import ProcessingConfig
from tests.utils.env_loader import load_env, get_oauth_config

# Load environment variables
load_env()

# Allow OAuth2 over HTTP for testing
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Export this so other tests can use it
TEST_OAUTH_CONFIG = get_oauth_config()

def test_oauth_pkce_auth():
    # Use existing config, just disable Spark requirement
    proc_config = ProcessingConfig(
        require_spark=False,
        require_duckdb=False
    )

    try:
        connector = ScalableSalesforceConnector(
            sf_config=TEST_OAUTH_CONFIG,
            processing_config=proc_config,
            log_level='DEBUG'
        )

        # Test connection with direct query
        results = connector.sf.query("SELECT Id FROM Account LIMIT 5")
        print("OAuth2 PKCE Auth Success:", results)

        # Test that we can get a simple record
        if results['records']:
            account_id = results['records'][0]['Id']
            account = connector.sf.Account.get(account_id)
            print(f"Successfully retrieved account: {account}")

    except Exception as e:
        print(f"OAuth2 PKCE Auth Failed: {str(e)}")
    finally:
        if 'connector' in locals():
            connector.close()

if __name__ == '__main__':
    test_oauth_pkce_auth() 