# Copyright 2025 GlyphyAI
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, TypeAlias, TypeGuard, TypeVar, Union, get_args, get_origin

from typing_extensions import TypeIs

if TYPE_CHECKING:
    # These are used to avoid mypy type errors with generic defaults.
    # When using TypeVar with a default value like:
    #   T = TypeVar("T", default=None)
    #   def func(value: T = None) -> None: ...
    # mypy incorrectly infers default value's type and complains it doesn't match T.
    # By erasing type information during type checking, we avoid these errors.
    _NoneType: Any = type(None)
    _None: Any = None
else:
    _NoneType = type(None)
    _None = None

T = TypeVar("T")
"""Type variable for generic types."""

JSON: TypeAlias = dict[str, Any] | list[Any] | str | float | int | bool | None
"""Type alias for JSON-compatible data structures."""


def union(types: Sequence[T]) -> Union[T]:  # noqa: UP007
    """Create a Union type from a sequence of types dynamically.

    This utility function creates a Union type from a sequence of types at runtime.
    It's useful when you need to create Union types dynamically based on a collection
    of types rather than specifying them statically.

    Args:
        types: A sequence of types to be combined into a Union type.
            The sequence can contain any valid Python types (classes, built-in types, etc.).

    Returns:
        A Union type combining all the provided types.

    Example:
        ```python
        # Create a Union type for int, str, and float
        number_types = [int, str, float]
        NumberUnion = union(number_types)  # Union[int, str, float]


        # Use in type hints
        def process_number(value: NumberUnion) -> None:
            pass


        # Create a Union type for custom classes
        class A:
            pass


        class B:
            pass


        custom_union = union([A, B])  # Union[A, B]
        ```

    Note:
        This function is particularly useful when working with dynamic type systems
        or when the set of types needs to be determined at runtime. For static type
        unions, it's recommended to use the standard `Union[T1, T2, ...]` syntax directly.
    """
    union: Any = Union[tuple(types)]  # noqa: UP007
    return union


def is_callable(obj: Any) -> TypeIs[Callable[..., Any]]:
    """Type guard for identifying callable objects, excluding class types.

    This function checks if an object is callable (like functions or methods) while
    specifically excluding class types, which are also technically callable.

    Args:
        obj: Object to check for callability.

    Returns:
        True if the object is a callable but not a class type, False otherwise.

    Example:
        ```python
        def my_func():
            pass


        class MyClass:
            pass


        is_callable(my_func)  # Returns True
        is_callable(MyClass)  # Returns False
        is_callable(print)  # Returns True
        ```
    """
    return callable(obj) and not isinstance(obj, type)


def is_subtype(obj: Any, obj_type: type[T]) -> TypeGuard[type[T]]:
    """Type guard for validating subclass relationships.

    This function performs a comprehensive check to ensure an object is a valid
    subclass of a target type, handling edge cases like None values and generic types.

    Args:
        obj: Object to check for subclass relationship.
        obj_type: Target type to validate against.

    Returns:
        True if obj is a valid subtype of obj_type, False otherwise.

    Example:
        ```python
        class Animal:
            pass


        class Dog(Animal):
            pass


        is_subtype(Dog, Animal)  # Returns True
        is_subtype(str, Animal)  # Returns False
        is_subtype(None, Animal)  # Returns False
        ```
    """
    origin = get_origin(obj_type)
    if origin is not None:
        return is_subtype(obj, origin)

    return obj is not None and not get_origin(obj) and isinstance(obj, type) and issubclass(obj, obj_type)


def supports_isinstance(type_: type) -> bool:
    """Check if a type supports isinstance checks.

    This is used for checking if a type supports isinstance checks, like checking
    if a tool's params_type supports isinstance checks.

    Args:
        type_: The type to check.

    Returns:
        True if the type supports isinstance checks.
    """
    metaclass = type(type_)
    return hasattr(metaclass, "__instancecheck__") or hasattr(metaclass, "__subclasscheck__")


def types_match(value_type: Any, expected_type: Any) -> bool:
    """Check if two types match structurally.

    This is used for comparing two types structurally, like checking if a tool's
    params_type matches an agent's params_type.

    Args:
        value_type: The type to compare.
        expected_type: The type to compare against.

    Returns:
        True if the types match structurally.
    """
    if isinstance(value_type, TypeVar) and isinstance(expected_type, TypeVar):
        # For TypeVars, we consider them equal if they have the same constraints
        return (
            value_type.__bound__ == expected_type.__bound__
            and value_type.__constraints__ == expected_type.__constraints__
            and value_type.__covariant__ == expected_type.__covariant__
            and value_type.__contravariant__ == expected_type.__contravariant__
        )
    elif isinstance(value_type, TypeVar) or isinstance(expected_type, TypeVar):
        # If one is a TypeVar and the other isn't, we consider them equal
        # This is a simplification but works for our use case where we're comparing
        # the same type variable from different instances
        return True

    # Get the base types (handles generics)
    value_origin = get_origin(value_type) or value_type
    expected_origin = get_origin(expected_type) or expected_type
    if value_origin != expected_origin:
        return False

    # If they're not generic types, we're done
    if not get_args(value_type) and not get_args(expected_type):
        return True

    # Compare generic parameters
    value_args = get_args(value_type)
    expected_args = get_args(expected_type)
    if len(value_args) != len(expected_args):
        return False

    return all(types_match(v, e) for v, e in zip(value_args, expected_args, strict=False))


def is_typed_dict(type_: Any) -> bool:
    """Check if a type is a TypedDict."""
    return hasattr(type_, "__annotations__") and hasattr(type_, "__total__")


def validate_type(type_: Any, expected_type: type) -> bool:
    """Validate that one type matches another type.

    This is used for comparing two types structurally, like checking if a tool's
    params_type matches an agent's params_type.

    Args:
        type_: The type to validate.
        expected_type: The type to validate against.

    Returns:
        True if the types match structurally.
    """
    return types_match(type_, expected_type)


def validate_value(value: Any, expected_type: type) -> bool:
    """Validate that a value matches an expected type.

    This is used for checking if a value is an instance of a type, like
    checking if context params match an agent's params_type.

    Args:
        value: The value to validate.
        expected_type: The type to validate against.

    Returns:
        True if the value matches the expected type.
    """
    if is_typed_dict(expected_type):
        return isinstance(value, dict)

    if supports_isinstance(expected_type):
        return isinstance(value, expected_type)

    return types_match(type(value), expected_type)
