"""قراردادهای معماری برای تمرین ABC، Protocol و Generic."""
from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar

T = TypeVar("T")


class BaseService(ABC):
    """قرارداد مشترک Serviceها."""

    @classmethod
    @abstractmethod
    def service_name(cls) -> str:
        """نام سرویس را برگرداند."""
        raise NotImplementedError


class RepositoryProtocol(Protocol[T]):
    """هر Repository باید بتواند یک شیء را ذخیره کند."""

    def add(self, item: T) -> None:
        ...


class SimpleRepository(Generic[T]):
    """یک Repository عمومی و ساده برای تمرین Generic.

    این کلاس برای داده‌های داخل حافظه است و به Excel وابسته نیست.
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def all(self) -> list[T]:
        return list(self._items)
