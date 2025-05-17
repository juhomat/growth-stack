"""Database Gateway port for database operations."""
from typing import Any, Dict, List, Optional, Protocol, Type, TypeVar, Union, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, Insert, Update, Delete

T = TypeVar('T')


class DBGateway(Protocol):
    """Interface for database gateway capabilities."""

    async def get_session(self) -> AsyncSession:
        """
        Get a database session.

        Returns:
            AsyncSession for database operations
        """
        ...

    async def execute(
        self,
        statement: Union[Select, Insert, Update, Delete],
        **kwargs: Any,
    ) -> Any:
        """
        Execute a SQL statement.

        Args:
            statement: SQLAlchemy statement to execute
            **kwargs: Additional parameters for execution

        Returns:
            Result of the execution
        """
        ...

    async def get_by_id(
        self,
        model: Type[T],
        id: Any,
        **kwargs: Any,
    ) -> Optional[T]:
        """
        Get a record by its ID.

        Args:
            model: SQLAlchemy model class
            id: Primary key value
            **kwargs: Additional parameters

        Returns:
            Record if found, None otherwise
        """
        ...

    async def create(
        self,
        model: Type[T],
        data: Dict[str, Any],
        **kwargs: Any,
    ) -> T:
        """
        Create a new record.

        Args:
            model: SQLAlchemy model class
            data: Dictionary of column values
            **kwargs: Additional parameters

        Returns:
            Created record
        """
        ...

    async def update(
        self,
        model: Type[T],
        id: Any,
        data: Dict[str, Any],
        **kwargs: Any,
    ) -> Optional[T]:
        """
        Update an existing record.

        Args:
            model: SQLAlchemy model class
            id: Primary key value
            data: Dictionary of column values to update
            **kwargs: Additional parameters

        Returns:
            Updated record if found, None otherwise
        """
        ...

    async def delete(
        self,
        model: Type[T],
        id: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Delete a record.

        Args:
            model: SQLAlchemy model class
            id: Primary key value
            **kwargs: Additional parameters

        Returns:
            True if deleted, False if not found
        """
        ... 