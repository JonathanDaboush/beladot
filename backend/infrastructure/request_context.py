from contextvars import ContextVar

_identity: ContextVar | None
try:
    _identity = ContextVar("identity", default=None)  # type: ignore[assignment]
except TypeError:
    # Fallback for older Python typings
    _identity = ContextVar("identity", default=None)


class _G:
    @property
    def user(self):
        return _identity.get()

    @user.setter
    def user(self, value):
        _identity.set(value)


g = _G()


def set_identity(identity):
    return _identity.set(identity)


def reset_identity(token):
    try:
        _identity.reset(token)
    except Exception:
        pass
