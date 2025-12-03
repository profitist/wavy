import uuid
from typing import TypeVar, Optional, Generic, Type

from app.core.database import Base
from app.repositories.base_repository import BaseRepo
from pydantic import BaseModel

service_type = TypeVar("service_type", bound=BaseRepo)


class BaseService(Generic[service_type]):
    def __init__(self, repository: service_type):
        self.repository = repository
