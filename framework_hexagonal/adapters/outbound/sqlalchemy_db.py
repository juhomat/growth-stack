"""SQLAlchemy adapter for DBGateway port."""
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast
import os
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import Select, Insert, Update, Delete
from sqlalchemy.orm import DeclarativeBase
from ...core.ports.db_gateway import DBGateway

T = TypeVar('T')


class SQLAlchemyDBAdapter:
    """SQLAlchemy implementation of the DBGateway port."""

    def __init__(
        self,
        connection_url: Optional[str] = None,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        **kwargs: Any,
    ):
        """
        Initialize the SQLAlchemy database adapter.

        Args:
            connection_url: SQLAlchemy connection URL (defaults to DATABASE_URL env var)
            echo: Whether to echo SQL statements
            pool_size: Connection pool size
            max_overflow: Maximum number of connections to create above pool_size
            **kwargs: Additional engine parameters
        """
        self.connection_url = connection_url or os.environ.get(
            "DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3"
        )
        self.engine = create_async_engine(
            self.connection_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            **kwargs,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    async def get_session(self) -> AsyncSession:
        """
        Get a database session.

        Returns:
            AsyncSession for database operations
        """
        return self.async_session_factory()

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
        async with self.get_session() as session:
            result = await session.execute(statement, **kwargs)
            if kwargs.get("commit", True):
                await session.commit()
            return result

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
        async with self.get_session() as session:
            stmt = select(model).where(model.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

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
        async with self.get_session() as session:
            instance = model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

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
        async with self.get_session() as session:
            instance = await self.get_by_id(model, id)
            if instance is None:
                return None
            
            for key, value in data.items():
                setattr(instance, key, value)
            
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

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
        async with self.get_session() as session:
            instance = await self.get_by_id(model, id)
            if instance is None:
                return False
            
            await session.delete(instance)
            await session.commit()
            return True 