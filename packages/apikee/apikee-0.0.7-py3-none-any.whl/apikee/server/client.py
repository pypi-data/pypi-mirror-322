import requests
from .error import handle_error
from .types import ApiKey, ApiResponse, Endpoint, Project


class ApiKeeClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    # ----------- PROJECT METHODS -----------

    def get_projects(self) -> list[Project]:
        try:
            response = requests.get(f"{self.base_url}/project", headers=self.headers)
            response.raise_for_status()
            return ApiResponse[Project].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def get_project_by_id(self, project_id: str) -> Project:
        try:
            response = requests.get(f"{self.base_url}/project/{project_id}", headers=self.headers)
            response.raise_for_status()
            return ApiResponse[Project].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def create_project(self, data: dict) -> Project:
        try:
            response = requests.post(f"{self.base_url}/project", json=data, headers=self.headers)
            response.raise_for_status()
            return ApiResponse[Project].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def update_project(self, project_id: str, data: dict) -> Project:
        try:
            response = requests.put(f"{self.base_url}/project/{project_id}", json=data, headers=self.headers)
            response.raise_for_status()
            return ApiResponse[Project].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def delete_project(self, project_id: str) -> None:
        try:
            response = requests.delete(f"{self.base_url}/project/{project_id}", headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            handle_error(e)

    # ----------- ENDPOINT METHODS -----------

    def get_endpoints(self) -> list[Endpoint]:
        try:
            response = requests.get(f"{self.base_url}/endpoint", headers=self.headers)
            response.raise_for_status()
            return ApiResponse[Endpoint].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def create_endpoint(self, data: dict) -> Endpoint:
        try:
            response = requests.post(f"{self.base_url}/endpoint", json=data, headers=self.headers)
            response.raise_for_status()
            return ApiResponse[Endpoint].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def delete_endpoint(self, endpoint_id: str) -> None:
        try:
            response = requests.delete(f"{self.base_url}/endpoint/{endpoint_id}", headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            handle_error(e)

    # ----------- API KEY METHODS -----------

    def get_api_keys(self) -> list[ApiKey]:
        try:
            response = requests.get(f"{self.base_url}/apikey", headers=self.headers)
            response.raise_for_status()
            return ApiResponse[ApiKey].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def create_api_key(self, name: str, project_id: str, endpoint_ids: list[str] = None) -> ApiKey:
        try:
            payload = {"name": name, "project_id": project_id, "endpoint_ids": endpoint_ids or []}
            response = requests.post(f"{self.base_url}/apikey", json=payload, headers=self.headers)
            response.raise_for_status()
            return ApiResponse[ApiKey].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def verify_api_key(self, key: str, endpoint_id: str) -> bool:
        try:
            payload = {"key": key, "endpoint_id": endpoint_id}
            response = requests.post(f"{self.base_url}/apikey/verify", json=payload, headers=self.headers)
            response.raise_for_status()
            return ApiResponse[bool].from_dict(response.json()).data
        except Exception as e:
            handle_error(e)

    def delete_api_key(self, api_key_id: str) -> None:
        try:
            response = requests.delete(f"{self.base_url}/apikey/{api_key_id}", headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            handle_error(e)
