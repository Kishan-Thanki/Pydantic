"""
Nested & Recursive Pydantic Models
=================================

This example demonstrates:
- Nested models (User → Address)
- Reusable data structures
- Recursive / self-referencing models (Comment → replies)
- Forward references and model rebuilding (Pydantic v2)

Libraries:
----------
pydantic.BaseModel
typing.List, typing.Optional

Official Documentation:
----------------------
https://docs.pydantic.dev/latest/concepts/models/#nested-models
https://docs.pydantic.dev/latest/concepts/models/#recursive-models
"""

from pydantic import BaseModel, ValidationError
from typing import List, Optional


# ======================================================
# ADDRESS MODEL — NESTED MODEL
# ======================================================

class Address(BaseModel):
    """
    Address model.

    Fields:
    -------
    street : str
        Street name and number

    city : str
        City name

    postal_code : str
        Postal/ZIP code
    """
    street: str
    city: str
    postal_code: str


# ======================================================
# USER MODEL — NESTED OBJECT
# ======================================================

class User(BaseModel):
    """
    User model containing a nested Address model.

    Fields:
    -------
    id : int
        Unique user identifier

    name : str
        Full name of the user

    address : Address
        Nested Address object
    """
    id: int
    name: str
    address: Address


# ======================================================
# COMMENT MODEL — RECURSIVE MODEL
# ======================================================

class Comment(BaseModel):
    """
    Comment model with recursive replies.

    Fields:
    -------
    id : int
        Unique comment identifier

    content : str
        Comment text

    replies : Optional[List[Comment]]
        List of nested replies (recursive structure)
        - Can be None or a list of Comment objects
    """
    id: int
    content: str
    replies: Optional[List["Comment"]] = None


# Required in Pydantic v2 to resolve forward references
Comment.model_rebuild()


# ======================================================
# MODEL INSTANTIATION
# ======================================================

try:
    # ✔ Creating Address instance
    address = Address(
        street="123 KingSt",
        city="Ahmedabad",
        postal_code="380001"
    )

    # ✔ Creating User with nested Address
    user = User(
        id=1,
        name="John Cena",
        address=address
    )

    # ✔ Creating recursive Comment structure
    comment = Comment(
        id=1,
        content="First Comment",
        replies=[
            Comment(id=2, content="Second Comment"),
            Comment(id=3, content="Third Comment")
        ]
    )

    print("User Object:")
    print(user)

    print("\nComment Thread:")
    print(comment)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Nested data does not match expected schema
    - Recursive structure is invalid
    - Type coercion fails
    """
    print("\nValidation Error Occurred:")
    print(e)
