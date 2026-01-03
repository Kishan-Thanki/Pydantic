"""
================================================================================
PYDANTIC — SPECIAL TYPES, SECURE FIELDS & ADVANCED VALIDATION
================================================================================

This example focuses on **advanced, real-world Pydantic features** that go
beyond basic type checking.

What this file demonstrates:

1. Automatic UUID generation using `default_factory`
2. Strongly typed, purpose-built fields:
   - EmailStr   → validated email addresses
   - HttpUrl    → validated URLs
   - SecretStr  → secure handling of sensitive values
3. Declarative constraints using `Annotated + Field`
4. Safe defaults for optional fields
5. Clear distinction between invalid and valid input
6. Validation that happens strictly at model instantiation

These patterns are common in:
- Authentication systems
- API schemas (FastAPI)
- Secure data models
- Production-grade backend services
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    SecretStr,
    ValidationError,
)

# ==============================================================================
# USER MODEL — SPECIAL PYDANTIC TYPES
# ==============================================================================

class User(BaseModel):
    """
    User schema demonstrating advanced Pydantic capabilities.

    Key characteristics:
    - Auto-generated UUID identifiers
    - Built-in validation for email and URLs
    - Secure password storage using SecretStr
    - Declarative constraints using Annotated
    """

    # Automatically generated unique identifier
    uid: UUID = Field(default_factory=uuid4)

    # Username must be between 3 and 20 characters
    username: Annotated[str, Field(min_length=3, max_length=20)]

    # Strict email validation
    email: EmailStr

    # Optional website, validated only if provided
    website: HttpUrl | None = None

    # Password is masked when printed or logged
    password: SecretStr

    # Age must be between 18 and 60
    age: Annotated[int, Field(ge=18, le=60)]

    # Optional and default fields
    bio: str = ""
    is_active: bool = True
    fullname: str | None = None
    createdAt: datetime | None = None


# ==============================================================================
# VALIDATION EXAMPLES
# ==============================================================================

# ------------------------------------------------------------------------------
# CASE 1: INVALID USER (MULTIPLE FAILURES)
# ------------------------------------------------------------------------------
try:
    user_invalid = User(
        username="j7",              # too short
        email="not-an-email",       # invalid email format
        password="weakpass",        # accepted as SecretStr, but hidden
        age=12,                     # below minimum age
    )

except ValidationError as e:
    print("Validation Error (Invalid User):")
    print(e)


# ------------------------------------------------------------------------------
# CASE 2: VALID USER
# ------------------------------------------------------------------------------
try:
    user_valid = User(
        username="jamesbond007",
        email="jamesbond@007.com",
        password="TopSecret007",
        age=40,
        website="https://007.com",
    )

    # Full validated model
    print(user_valid)
    # uid=UUID('1b33320c-24a2-45e1-8c93-82100cc14bb5') username='jamesbond007' email='jamesbond@007.com' website=HttpUrl('https://007.com/') password=SecretStr('**********') age=40 bio='' is_active=True fullname=None createdAt=None

    # Password is masked by default
    # Password (masked): **********
    print("Password (masked):", user_valid.password)

    # Explicit access to raw secret value
    # Password (raw): TopSecret007
    print("Password (raw):", user_valid.password.get_secret_value())

    # Output:

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

- UUIDs should be generated with `default_factory`, not manually assigned
- Purpose-built types (EmailStr, HttpUrl, SecretStr) prevent entire classes of bugs
- `Annotated + Field` keeps validation rules declarative and readable
- Sensitive data is protected by default
- Validation occurs only at model creation — invalid data never leaks in

This is how Pydantic enables **secure, explicit, production-ready schemas**
without writing custom validation logic.
================================================================================
"""
