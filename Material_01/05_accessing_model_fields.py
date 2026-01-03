"""
================================================================================
PYDANTIC — ACCESSING & MUTATING MODEL FIELDS
================================================================================

Goal:
- Show how to access fields from a validated Pydantic model
- Demonstrate default mutability behavior
- Highlight that reassignment does NOT trigger re-validation by default

Key point:
Pydantic validates data at model creation, not on every attribute assignment.
"""

from datetime import datetime

from pydantic import BaseModel, ValidationError

# ==============================================================================
# SCHEMA DEFINITION
# ==============================================================================

class User(BaseModel):
    """
    User schema.
    """

    uid: int
    username: str
    email: str
    age: int

    bio: str = ""
    is_active: bool = True

    fullname: str | None = None
    createdAt: datetime | None = None


# ==============================================================================
# MODEL CREATION, ACCESS, AND MUTATION
# ==============================================================================

try:
    user = User(
        uid=101,
        username="jamesbond007",
        email="jamesbond@007.com",
        age=40,
    )

    # Print the full validated model
    print(user)
    # uid=101 username='jamesbond007' email='jamesbond@007.com'
    # age=40 bio='' is_active=True fullname=None createdAt=None

    # Access a specific field
    print(user.username)   # jamesbond007

    # --------------------------------------------------------------------------
    # MUTATING FIELDS AFTER CREATION
    # --------------------------------------------------------------------------

    # Pydantic models are mutable by default
    # Re-assigning a field does NOT trigger validation
    user.bio = 123         # type mismatch (int assigned to str)
    print(user.bio)        # 123

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

- Model fields are accessed via dot notation
- Models are mutable by default
- Attribute reassignment does NOT re-validate types
- Validation happens only at instantiation

This behavior is intentional and important to understand when
using Pydantic models in long-lived objects or stateful systems.
================================================================================
"""
