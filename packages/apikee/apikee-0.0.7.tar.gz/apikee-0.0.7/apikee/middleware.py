from config import config
from security import generate_key, validate_key
from server.client import ApiKeeClient

def generate_api_key(name: str, project_id=None, endpoint_ids=None):
    """Generate an API key (local or managed)."""
    if not name:
        raise ValueError("Invalid Request: `name` is required to generate an API key.")

    # Managed Key
    if project_id:
        if not config['host'] or not config['project'] or not config['token']:
            raise ValueError("Configuration Error: `host`, `project`, and `token` must be configured for server validation.")
        
        client = ApiKeeClient(f"https://{config['host']}/api/v1", config['token'])
        return client.create_api_key(name, project_id, endpoint_ids)

    # Local Key
    return generate_key(name)


def validate_api_key(apikey: str, key_id=None, endpoint_id=None):
    """Validate an API key (local or managed)."""
    if not apikey:
        raise ValueError("Invalid Request: `apikey` is required for validation.")

    if endpoint_id and key_id:
        raise ValueError("Invalid Request: Both `endpoint_id` and `key_id` are provided. Please specify only one.")

    # Managed Key
    if endpoint_id and not key_id:
        if not config['host'] or not config['project'] or not config['token']:
            raise ValueError("Configuration Error: `host`, `project`, and `token` must be configured for server validation.")
        
        client = ApiKeeClient(f"https://{config['host']}/api/v1", config['token'])
        return client.verify_api_key(apikey, endpoint_id)

    # Local Key
    if not endpoint_id and key_id:
        return validate_key(apikey, key_id)

    raise ValueError("Invalid Request: Either `endpoint_id` or `key_id` must be provided for validation.")