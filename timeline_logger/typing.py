from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from typing import TYPE_CHECKING, Any, Protocol

from django.db import models

from typing_extensions import TypeIs

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser


type EventDict = MutableMapping[str, Any]
"""
Structlog's ``EventDict`` type, vendored to avoid a dependency.

See upstream: https://github.com/hynek/structlog/blob/811245fe02fcf454f517f0677648457bfec52ef0/src/structlog/typing.py#L57
"""


class EventDetailsProtocol[U: AbstractBaseUser](Protocol):
    """
    Dataclass or similar that can provide the timeline logger event details.
    """

    instance: models.Model

    def get_template_name(self) -> str: ...
    def get_user(self) -> U | None: ...
    def get_extra_data(self) -> Mapping[str, object]: ...


class Adapter(Protocol):
    def __call__(self, event_dict: EventDict) -> EventDetailsProtocol | None: ...


def is_event_dict(msg: str | Any) -> TypeIs[EventDict]:
    """
    Test if the provided log record message is an event dict.
    """
    return isinstance(msg, dict)
