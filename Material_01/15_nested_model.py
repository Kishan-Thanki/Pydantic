"""
================================================================================
PYDANTIC — IMMUTABLE MODELS, NESTED DATA & COMPUTED FIELDS (ADVANCED)
================================================================================

This example demonstrates:

1. Creating **User** and **BlogPost** with NEW VALUES
2. Nested model validation (User inside BlogPost)
3. Alias usage (`id` -> `uid`)
4. Strict + frozen models (immutability)
5. Computed fields (`display_name`, `is_influencer`)
6. Default factories for timestamps
7. Why reassignment is NOT allowed when `frozen=True`

IMPORTANT:
---------
Because `User` is declared with `frozen=True`,
instances are **immutable**.
You CANNOT do:
    user.email = "new@email.com"

Instead, you must:
- Create a NEW instance
- Or use `model_copy(update={...})`
================================================================================
"""

import json
from datetime import UTC, datetime
from functools import partial
from typing import Annotated, List, Literal
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    SecretStr,
    computed_field,
    field_validator,
)

# ==============================================================================
# USER MODEL (IMMUTABLE)
# ==============================================================================

class User(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        extra="allow",
        validate_assignment=True,
        frozen=True,              # IMMUTABLE
    )

    uid: UUID = Field(alias="id", default_factory=uuid4)

    username: Annotated[str, Field(min_length=3, max_length=20)]
    email: EmailStr
    password: SecretStr
    website: HttpUrl | None = None
    age: Annotated[int, Field(ge=13, le=130)]
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True

    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0

    # --------------------------------------------------------------------------
    # VALIDATORS
    # --------------------------------------------------------------------------

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()

    @field_validator("website", mode="before")
    @classmethod
    def add_https(cls, v: str | None) -> str | None:
        if v and not v.startswith(("http://", "https://")):
            return f"https://{v}"
        return v

    # --------------------------------------------------------------------------
    # COMPUTED FIELDS
    # --------------------------------------------------------------------------

    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 10_000


# ==============================================================================
# COMMENT MODEL
# ==============================================================================

class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0


# ==============================================================================
# BLOG POST MODEL
# ==============================================================================

class BlogPost(BaseModel):

    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10)]

    # Nested User model
    author: User

    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    create_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))
    status: Literal["draft", "published", "archived"] = "draft"
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]

    comments: List[Comment] = Field(default_factory=list)


# ==============================================================================
# CREATE BLOG POST (WITH NEW VALUES)
# ==============================================================================

post_data = {
    "title": "Deep Dive into Pydantic v2",
    "content": "Pydantic v2 introduces computed fields, validators, and immutability.",
    "slug": "deep-dive-pydantic-v2",
    "author": {
        "id": "a1f8b7c1-9d77-4c9a-8c2c-7c2f01aa9999",
        "username": "jamesbond007",
        "email": "jamesbond@007.com",
        "password": "UltraSecret!",
        "age": 42,
        "first_name": "James",
        "last_name": "Bond",
        "follower_count": 25000,
        "website": "jamesbond.007",
    },
    "comments": [
        {
            "content": "This explanation is crystal clear!",
            "author_email": "reader1@example.com",
            "likes": 40,
        },
        {
            "content": "What to lear next!.",
            "author_email": "reader2@example.com",
            "likes": 18,
        },
    ],
}

post = BlogPost.model_validate(post_data)

print("BLOG POST:")
print(post.model_dump_json(indent=2))


# ==============================================================================
# CREATE USER (WITH NEW VALUES)
# ==============================================================================

user_data = {
    "id": "7b2a9a5d-6e6b-4db6-92c9-8c71c2e4abcd",
    "username": "Python_Master",
    "email": "pythonmaster@example.com",
    "password": "MasterKey123",
    "age": 35,
    "first_name": "Python",
    "last_name": "Master",
    "follower_count": 5200,
    "notes": "Loves clean architecture",
}

user = User.model_validate_json(json.dumps(user_data))

print("\nUSER:")
print(user.model_dump_json(indent=2))


# ==============================================================================
# IMMUTABILITY DEMO (CORRECT WAY)
# ==============================================================================

# This would FAIL (frozen=True)
# user.email = "new@email.com"

# Correct approach: create a NEW instance
updated_user = user.model_copy(update={"email": "pythonmaster@newmail.com"})

print("\nUPDATED USER (NEW INSTANCE):")
print(updated_user.model_dump_json(indent=2))


"""
--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

1. `frozen=True` makes models IMMUTABLE (production-safe)
2. Nested models validate recursively
3. Aliases (`id -> uid`) work seamlessly
4. Computed fields are serialized automatically
5. Updates require `model_copy(update=...)`
6. This pattern is ideal for:
   - Event-driven systems
   - Audit-safe data
   - CQRS / DDD architectures

This is **real-world, enterprise-grade Pydantic modeling**.
================================================================================
"""
