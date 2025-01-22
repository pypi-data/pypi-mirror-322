# Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
#
# SPDX-License-Identifier: Apache-2.0


from abc import ABC
from typing import Annotated, Any, Callable, Literal, Optional, Type, TypeVar, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, create_model

PetType = TypeVar("PetType", bound=Literal["cat", "dog"])

__all__ = ["BaseMessage", "wrap_message", "get_annotated_type_for_message_classes"]


class BaseMessage(BaseModel, ABC):
    uuid: UUID

    def __init__(self, uuid: Optional[UUID] = None, **kwargs: Any) -> None:
        uuid = uuid or uuid4()
        super().__init__(uuid=uuid, **kwargs)

    def print(self, f: Optional[Callable[..., Any]] = None) -> None:
        """Print message

        Args:
            f (Optional[Callable[..., Any]], optional): Print function. If none, python's default print will be used.
        """
        ...


def camel2snake(name: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


_message_classes: dict[str, Type[BaseModel]] = {}


def wrap_message(message_cls: Type[BaseMessage]) -> Type[BaseModel]:
    """Wrap a message class with a type field to be used in a union type

    This is needed for proper serialization and deserialization of messages in a union type.

    Args:
        message_cls (Type[BaseMessage]): Message class to wrap
    """
    global _message_classes

    if not message_cls.__name__.endswith("Message"):
        raise ValueError("Message class name must end with 'Message'")

    type_name = camel2snake(message_cls.__name__)
    type_name = type_name[: -len("_message")]

    class WrapperBase(BaseModel):
        # these types are generated dynamically so we need to disable the type checker
        type: Literal[type_name] = type_name  # type: ignore[valid-type]
        content: message_cls  # type: ignore[valid-type]

        def __init__(self, *args: Any, **data: Any):
            if set(data.keys()) == {"type", "content"} and "content" in data:
                super().__init__(*args, **data)
            else:
                if "content" in data:
                    content = data.pop("content")
                    super().__init__(*args, content=message_cls(*args, **data, content=content), **data)
                else:
                    super().__init__(content=message_cls(*args, **data), **data)

        def print(self, f: Optional[Callable[..., Any]] = None) -> None:
            self.content.print(f)  # type: ignore[attr-defined]

    Wrapper = create_model(message_cls.__name__, __base__=WrapperBase)

    _message_classes[type_name] = Wrapper

    return Wrapper


def get_annotated_type_for_message_classes() -> Type[Any]:
    # this is a dynamic type so we need to disable the type checker
    union_type = Union[tuple(_message_classes.values())]  # type: ignore[valid-type]
    return Annotated[union_type, Field(discriminator="type")]  # type: ignore[return-value]


def get_message_classes() -> dict[str, Type[BaseModel]]:
    return _message_classes
