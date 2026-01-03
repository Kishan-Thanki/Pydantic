"""
================================================================================
PYDANTIC — DEFAULT_FACTORY, MUTABLE DEFAULTS & LITERAL TYPES
================================================================================

This example demonstrates several *important but non-obvious* Pydantic concepts:

1. Why mutable defaults (like lists) must use `default_factory`
2. Why dynamic values (like datetime.now) must NOT be used directly
3. How `default_factory` executes at **instance creation time**
4. How `Literal` restricts values to a fixed set
5. How Pydantic handles flexible union types (str | int)

These patterns are essential for writing *correct, bug-free schemas*.
"""

from datetime import UTC, datetime
from functools import partial
from typing import List, Literal

from pydantic import BaseModel, Field, ValidationError

# ==============================================================================
# SCHEMA DEFINITION
# ==============================================================================

class BlogPost(BaseModel):
    """
    BlogPost schema illustrating:
    - Safe defaults
    - Runtime-generated values
    - Restricted field values
    """

    # ---------------------------
    # REQUIRED FIELDS
    # ---------------------------
    bpid: int
    title: str
    content: str
    author_id: str | int   # Accepts either int or string IDs

    # ---------------------------
    # DEFAULT SCALAR FIELDS
    # ---------------------------
    view_count: int = 0
    is_published: bool = False

    # ---------------------------
    # MUTABLE DEFAULT (CORRECT WAY)
    # ---------------------------
    tags: List[str] = Field(default_factory=list)

    """
    BAD PRACTICE (do NOT do this):
        tags: List[str] = []

    Why?
    - Lists are mutable
    - The same list would be shared across all instances
    """

    # ---------------------------
    # RUNTIME DATETIME DEFAULT
    # ---------------------------
    createAt: datetime = Field(
        default_factory=partial(datetime.now, tz=UTC)
    )

    """
    BAD PRACTICE:
        createAt: datetime = datetime.now(UTC)

    Why?
    - Executed once at class definition time
    - Every instance would get the SAME timestamp
    """

    # ---------------------------
    # RESTRICTED VALUE FIELD
    # ---------------------------
    status: Literal["draft", "publish", "archive"] = "draft"


# ==============================================================================
# MODEL CREATION
# ==============================================================================

try:
    blog_post = BlogPost(
        bpid=201,
        title="Writing my first post",
        content="This is nothing in this post",
        author_id=101,
    )

    print(blog_post)

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

1. Use `default_factory` for:
   - Mutable defaults (list, dict, set)
   - Dynamic values (datetime.now, uuid, etc.)

2. Never assign:
   - [] or {} directly as defaults
   - datetime.now() directly as a default

3. `Literal` enforces strict allowed values
   - Anything outside the defined set raises an error

4. `partial()` is a clean way to pass arguments to factory functions

These rules prevent subtle bugs that are very hard to detect later.
================================================================================
"""