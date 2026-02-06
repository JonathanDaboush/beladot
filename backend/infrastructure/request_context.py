from contextvars import ContextVar
from typing import Any, Optional

_identity: ContextVar[Optional[dict[str, Any]]] = ContextVar("identity", default=None)


class _G:
    @property
    def user(self) -> Optional[dict[str, Any]]:
        return _identity.get()

    @user.setter
    def user(self, value: Optional[dict[str, Any]]) -> None:
        _identity.set(value)


g = _G()


def set_identity(identity):
    return _identity.set(identity)


def reset_identity(token):
    try:
        _identity.reset(token)
    except LookupError as e:
        try:
            from backend.infrastructure.structured_logging import logger
            logger.debug("request_context.reset_failed", error=str(e))
        except Exception:
            pass
