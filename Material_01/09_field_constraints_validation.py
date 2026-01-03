"""
================================================================================
PYDANTIC — FIELD CONSTRAINTS USING Annotated & VALIDATION RULES
================================================================================

This example demonstrates:

1. How to enforce **field constraints** using `Annotated` and `Field`
2. How Pydantic validates values at runtime
3. Combining constraints with defaults, mutable fields, and literals
4. Patterns for strings (regex) using `pattern`
"""

from datetime import UTC, datetime
from functools import partial
from typing import Annotated, List, Literal

from pydantic import BaseModel, Field, ValidationError

# ==============================================================================
# USER MODEL WITH CONSTRAINTS
# ==============================================================================

class User(BaseModel):
    """
    User schema with validation constraints:
    - uid >= 0
    - username: 3–20 characters
    - age: 18–60
    """

    uid: Annotated[int, Field(ge=0)]                  # Must be integer >= 0
    username: Annotated[str, Field(min_length=3, max_length=20)]
    email: str
    age: Annotated[int, Field(ge=18, le=60)]          # Must be between 18 and 60

    # Optional/default fields
    bio: str = ""
    is_active: bool = True
    fullname: str | None = None
    createdAt: datetime | None = None


# ==============================================================================
# BLOG POST MODEL WITH PATTERN & DEFAULTS
# ==============================================================================

class BlogPost(BaseModel):
    """
    BlogPost schema demonstrating:
    - default values
    - mutable defaults with default_factory
    - runtime datetime defaults
    - literal constraints
    - regex pattern validation
    """

    bpid: int
    title: str
    content: str
    author_id: str | int

    view_count: int = 0
    is_published: bool = False

    # Correctly handle mutable default
    tags: List[str] = Field(default_factory=list)

    # Runtime datetime
    createAt: datetime = Field(default_factory=partial(datetime.now, tz=UTC))

    # Restrict status values
    status: Literal["draft", "publish", "archive"] = "draft"

    # String must match regex pattern
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]


# ==============================================================================
# MODEL CREATION & VALIDATION
# ==============================================================================

try:
    # Invalid user (uid >= 0, username length, age range)
    user_invalid = User(
        uid=0,
        username="j7",             # too short
        email="jamesbond@007.com",
        age=12,                    # below minimum
    )

except ValidationError as e:
    print("Validation Error (Invalid User):")
    print(e)

try:
    # Valid user
    user_valid = User(
        uid=101,
        username="jamesbond007",
        email="jamesbond@007.com",
        age=40,
    )
    print(user_valid)

    # Blog post
    blog_post = BlogPost(
        bpid=201,
        title="Writing my first post",
        content="This is nothing in this post",
        author_id=101,
        slug="writing-my-first-post"
    )
    print(blog_post)

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

1. Use `Annotated[type, Field(...)]` to enforce constraints:
   - `ge`, `le` for numeric bounds
   - `min_length`, `max_length` for strings
   - `pattern` for regex validation

2. Validation occurs **at object creation**:
   - Invalid values immediately raise a `ValidationError`

3. Combining constraints with:
   - Defaults
   - Optional fields
   - Mutable fields
   - Literal values

4. Provides robust, declarative, and maintainable validation logic
   without writing any manual checks.
================================================================================
"""
