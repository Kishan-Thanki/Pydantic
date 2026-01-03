"""
================================================================================
PYDANTIC — FIELD VALIDATORS & DATA NORMALIZATION
================================================================================

This example introduces **custom validation logic** using Pydantic v2
validators, while still keeping the model clean and declarative.

Concepts demonstrated:

1. `field_validator` for field-level validation
2. Data normalization (e.g., lowercasing usernames)
3. Custom validation rules beyond basic type checks
4. `mode="before"` validation for preprocessing input
5. Secure handling of sensitive fields
6. Clear separation of schema, validation, and usage

These techniques are essential when:
- Built-in constraints are not enough
- Input data must be normalized
- Business rules must be enforced early
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
    field_validator,
)

# ==============================================================================
# USER MODEL WITH CUSTOM VALIDATORS
# ==============================================================================

class User(BaseModel):
    """
    User schema demonstrating custom field validation.

    Enhancements added:
    - Username normalization and character restrictions
    - Automatic URL normalization
    - Strong typing with built-in Pydantic types
    """

    # ---------------------------
    # CORE FIELDS
    # ---------------------------
    uid: UUID = Field(default_factory=uuid4)
    username: Annotated[str, Field(min_length=3, max_length=20)]
    email: EmailStr
    website: HttpUrl | None = None
    password: SecretStr
    age: Annotated[int, Field(ge=18, le=60)]

    # ---------------------------
    # OPTIONAL / DEFAULT FIELDS
    # ---------------------------
    bio: str = ""
    is_active: bool = True
    fullname: str | None = None
    createdAt: datetime | None = None

    # --------------------------------------------------------------------------
    # FIELD VALIDATORS
    # --------------------------------------------------------------------------

    @field_validator("username")
    @classmethod
    def validate_and_normalize_username(cls, value: str) -> str:
        """
        Enforce username rules:
        - Only alphanumeric characters and underscores are allowed
        - Username is normalized to lowercase
        """
        if not value.replace("_", "").isalnum():
            raise ValueError(
                "Username must be alphanumeric (underscores allowed)"
            )
        return value.lower()

    @field_validator("website", mode="before")
    @classmethod
    def normalize_website_url(cls, value: str | None) -> str | None:
        """
        Ensure website URLs always include a scheme.

        This runs BEFORE standard validation, allowing us to
        modify raw input safely.
        """
        if value and not value.startswith(("http://", "https://")):
            return f"https://{value}"
        return value


# ==============================================================================
# VALIDATION EXAMPLES
# ==============================================================================
try:
    user_valid = User(
        username="James_Bond007",   # normalized to lowercase
        email="jamesbond@007.com",
        password="TopSecret007",
        age=40,
        website="007.com",          # scheme auto-added
    )

    print(user_valid)
    print("Password (masked):", user_valid.password)
    print("Password (raw):", user_valid.password.get_secret_value())

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

1. `field_validator` lets you enforce domain-specific rules
2. Validators can normalize data, not just reject it
3. `mode="before"` is ideal for preprocessing raw input
4. Built-in types + custom validators cover most real-world needs
5. Validation remains centralized and predictable

This is the final step toward **fully expressive, production-ready
Pydantic models**.
================================================================================
"""
