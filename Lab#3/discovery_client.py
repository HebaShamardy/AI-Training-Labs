# discovery_client.py

import os
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

# Get Watson Discovery credentials from environment variables
DISCOVERY_APIKEY = os.getenv("DISCOVERY_APIKEY")
DISCOVERY_URL = os.getenv("DISCOVERY_URL")
DISCOVERY_PROJECT_ID = os.getenv("DISCOVERY_PROJECT_ID") # Your Discovery Project ID
DISCOVERY_COLLECTION_ID = os.getenv("DISCOVERY_COLLECTION_ID") # Your Discovery Collection ID

# Watson Discovery authenticator and client
authenticator = None
discovery = None

def connect_discovery():
    """Establishes connection to Watson Discovery."""
    global authenticator, discovery
    if not DISCOVERY_APIKEY or not DISCOVERY_URL or not DISCOVERY_PROJECT_ID:
        print("Watson Discovery credentials or IDs not found in environment variables.")
        return False
    try:
        authenticator = IAMAuthenticator(DISCOVERY_APIKEY)
        discovery = DiscoveryV2(
            version='2020-08-01', # Use the appropriate API version
            authenticator=authenticator
        )
        discovery.set_service_url(DISCOVERY_URL)
        print("Connected to Watson Discovery successfully!")
        return True
    except Exception as e:
        print(f"Error connecting to Watson Discovery: {e}")
        return False


def query_discovery(query_text: str, product_id: str = None):
    """Queries the Watson Discovery collection."""
    if discovery is None:
        print("Watson Discovery client not initialized.")
        return None
    try:
        # Construct the query parameters
        query_params = {
            'query': query_text,
            'count': 10 # Number of results to return
        }

        # If product_id is provided, add a filter for it
        if product_id:
            query_params['filter'] = f'product_id::{product_id}'

        query_response = discovery.query(
            project_id=DISCOVERY_PROJECT_ID,
            **query_params
        ).get_result()

        print(f"Query successful. Found {query_response.get('matching_results')} results.")
        return query_response
    except Exception as e:
        print(f"Error querying Discovery: {e}")
        return None

