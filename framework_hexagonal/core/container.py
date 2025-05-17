"""Dependency injection container for port implementations."""
from typing import Dict, Type, TypeVar, Any, Optional, cast, get_type_hints

T = TypeVar('T')


class Container:
    """
    Container for managing port implementations.
    
    This container allows applications to register and retrieve
    adapter implementations for port interfaces.
    """

    def __init__(self) -> None:
        """Initialize an empty container."""
        self._registry: Dict[Type[Any], Any] = {}

    def register(self, port_type: Type[T], implementation: Any) -> None:
        """
        Register an implementation for a port type.

        Args:
            port_type: The port interface type
            implementation: An instance implementing the port interface
        """
        self._registry[port_type] = implementation

    def get(self, port_type: Type[T]) -> T:
        """
        Get the implementation for a port type.

        Args:
            port_type: The port interface type

        Returns:
            The registered implementation for the port

        Raises:
            KeyError: If no implementation is registered for the port type
        """
        if port_type not in self._registry:
            raise KeyError(f"No implementation registered for {port_type.__name__}")
        return cast(T, self._registry[port_type])

    def has(self, port_type: Type[T]) -> bool:
        """
        Check if an implementation is registered for a port type.

        Args:
            port_type: The port interface type

        Returns:
            True if an implementation is registered, False otherwise
        """
        return port_type in self._registry


# Global container instance for convenience
container = Container() 