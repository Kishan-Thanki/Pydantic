"""
================================================================================
PYDANTIC — COMPUTED FIELDS & DERIVED DATA
================================================================================

This example introduces **computed fields**, which allow you to expose
derived, read-only values on a Pydantic model without storing them directly.

Concepts demonstrated:

1. `computed_field` for derived attributes
2. Read-only properties included in serialization
3. Model-level validation (password confirmation)
4. Clean separation between stored data and derived data
5. Business logic expressed declaratively inside the model

Computed fields are ideal for:
- Display values (full names, labels)
- Flags derived from numeric thresholds
- Aggregated or formatted data
"""

from pydantic import (
    BaseModel,
    EmailStr,
    ValidationError,
    computed_field,
    model_validator,
)

# ==============================================================================
# USER REGISTRATION MODEL
# ==============================================================================

class UserRegistration(BaseModel):
    """
    User registration schema demonstrating computed fields.

    Stored fields:
    - Raw user input
    - Authentication-related data

    Computed fields:
    - display_name
    - is_influencer
    """

    # ---------------------------
    # PROFILE DATA
    # ---------------------------
    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0

    # ---------------------------
    # AUTHENTICATION DATA
    # ---------------------------
    email: EmailStr
    password: str
    confirm_password: str

    # --------------------------------------------------------------------------
    # MODEL VALIDATOR (CROSS-FIELD)
    # --------------------------------------------------------------------------

    @model_validator(mode="after")
    def passwords_match(self) -> "UserRegistration":
        """
        Ensure password and confirm_password are identical.
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

    # --------------------------------------------------------------------------
    # COMPUTED FIELDS (DERIVED VALUES)
    # --------------------------------------------------------------------------

    @computed_field
    @property
    def display_name(self) -> str:
        """
        Human-friendly display name.

        Priority:
        1. first_name + last_name (if available)
        2. email prefix as fallback
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email.split("@")[0]

    @computed_field
    @property
    def is_influencer(self) -> bool:
        """
        Determines influencer status based on follower count.
        """
        return self.follower_count >= 10_000


# ==============================================================================
# USAGE EXAMPLE
# ==============================================================================

try:
    user = UserRegistration(
        first_name="James",
        last_name="Bond",
        follower_count=15000,
        email="jamesbond@007.com",
        password="TopSecret007",
        confirm_password="TopSecret007",
    )

    print("User registration successful:")
    print(user.model_dump_json(indent=2))
    print("Display name:", user.display_name)
    print("Is influencer:", user.is_influencer)

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

1. `computed_field` creates read-only, derived attributes
2. Computed fields:
   - Are NOT stored
   - ARE included in serialization (`model_dump`)
3. Perfect for business logic that depends on multiple fields
4. Keeps models expressive without duplicating data
5. Complements field & model validators cleanly

Together with validators, computed fields make Pydantic models:
✔ Declarative
✔ Consistent
✔ Business-aware

This is the final layer of **rich, production-grade Pydantic modeling**.
================================================================================
"""
