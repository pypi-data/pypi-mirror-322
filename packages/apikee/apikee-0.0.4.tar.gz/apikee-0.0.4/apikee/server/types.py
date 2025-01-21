from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T
    error: Optional[str] = None


class Project(BaseModel):
    id: str
    is_active: bool
    prod_id: Optional[str]
    api_kee_id: Optional[str]
    name: str
    desc: Optional[str]


class Endpoint(BaseModel):
    id: str
    is_active: bool
    path: str
    method: str
    desc: Optional[str]
    project_id: str
    created_at: str
    updated_at: str


class ApiKey(BaseModel):
    id: str
    is_active: bool
    key: str
    name: str
    status: str
    project_id: str
    created_at: str
    updated_at: str
    expires_at: Optional[str]
