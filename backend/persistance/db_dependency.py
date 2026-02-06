"""Database dependency shim.

Re-export the centralized async session dependency from
`backend.persistance.async_base` so the rest of the codebase can
import `get_db` and receive a properly-typed `AsyncSession`.
"""

from .async_base import get_async_session

# Backwards compatible name expected by other modules
get_db = get_async_session
