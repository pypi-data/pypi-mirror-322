from abc import ABC
from typing import Generic, TypeVar, Optional
from django.db.models import QuerySet

R = TypeVar("R")


class BaseService(ABC, Generic[R]):
    def __init__(self, repository: R):
        self._repository = repository

    def get_all(self) -> QuerySet:
        """Fetch all objects."""
        return self._repository.get_all()

    def get_by_id(self, obj_id: int) -> Optional[T]:
        """Fetch a single object by ID."""
        return self._repository.get_by_id(obj_id)

    def create(self, data: Optional[dict] = None, **kwargs):
        """
        Create a new object.
        Supports both a dictionary (`data`) or keyword arguments (`**kwargs`).
        """
        return self._repository.create(data, **kwargs)

    def update(self, obj_id: int, data: dict):
        """Update an object with the given data."""
        return self._repository.update(obj_id, data)

    def delete(self, obj_id: int) -> bool:
        """Delete an object by ID."""
        return self._repository.delete(obj_id)

    def filter(self, **filters) -> QuerySet:
        """Filter objects based on given criteria."""
        return self._repository.filter(**filters)

    def exists(self, **kwargs) -> bool:
        """Check if an object exists with the given criteria."""
        return self._repository.exists(**kwargs)

    def count(self, **kwargs) -> int:
        """Count objects with the given criteria."""
        return self._repository.count(**kwargs)

    def get_or_create(self, defaults: Optional[dict] = None, **kwargs):
        """Get or create an object with the given criteria."""
        return self._repository.get_or_create(defaults, **kwargs)
