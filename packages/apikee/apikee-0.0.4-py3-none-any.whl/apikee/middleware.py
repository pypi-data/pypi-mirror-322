from apikee.config import Config
from apikee.security import generate_key, validate_key
from apikee.server.client import ApiKeeClient

def generate_api_key(name: str, project_id: str = None, endpoint_ids: list = None) -> dict:
    if not name:
        raise ValueError("Missing apikey name.")

    if project_id:
        if not all([Config.host, Config.token, Config.project]):
            raise ValueError("Project validation requires host, token, and project to be configured.")
        client = ApiKeeClient(f"https://{Config.host}/api/v1", Config.token)
        return client.create_api_key(name, project_id, endpoint_ids)

    return generate_key(name)


def validate_api_key(api_key: str, key_id: str = None, endpoint_id: str = None) -> bool:
    if not api_key:
        raise ValueError("Missing apikey.")
    if endpoint_id and key_id:
        raise ValueError("Specify either endpoint_id or key_id, not both.")

    if endpoint_id:
        if not all([Config.host, Config.token, Config.project]):
            raise ValueError("Project validation requires host, token, and project to be configured.")
        client = ApiKeeClient(f"https://{Config.host}/api/v1", Config.token)
        return client.verify_api_key(api_key, endpoint_id)

    if key_id:
        return validate_key(api_key, key_id)

    raise ValueError("Invalid arguments provided.")
