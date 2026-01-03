"""
================================================================================
PYDANTIC — TYPE COERCION (AUTOMATIC TYPE CONVERSION)
================================================================================

This example demonstrates an important Pydantic behavior:

Pydantic performs **type coercion by default**.

Meaning:
- If input data can be *reasonably converted* to the expected type,
  Pydantic will convert it instead of raising an error.
- If conversion does NOT make sense, a ValidationError is raised.

This is intentional and helps when dealing with real-world input
(e.g., JSON, environment variables, form data).
"""

from datetime import datetime

from pydantic import BaseModel, ValidationError

# ==============================================================================
# SCHEMA DEFINITION
# ==============================================================================

class User(BaseModel):
    """
    User schema demonstrating type coercion.
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
# TYPE COERCION IN ACTION
# ==============================================================================

try:
    user = User(
        uid="101",        # ❗ Provided as string, expected int
        username="jamesbond007",
        email="jamesbond@007.com",
        age=40,
    )

    # --------------------------------------------------------------------------
    # OBSERVED BEHAVIOR
    # --------------------------------------------------------------------------

    # Pydantic successfully creates the model
    print(user)
    # uid=101 username='jamesbond007' email='jamesbond@007.com'
    # age=40 bio='' is_active=True fullname=None createdAt=None

    # Accessing the field
    print(user.uid)          # 101

    # Confirming the type after validation
    print(type(user.uid))    # <class 'int'>

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
WHAT JUST HAPPENED?
--------------------------------------------------------------------------------

- `uid` was provided as a string: "101"
- The schema expects an int
- Pydantic detected that:
    • "101" can be safely converted to int
- Conversion was applied automatically

This behavior is called **type coercion**.

--------------------------------------------------------------------------------
WHEN DOES PYDANTIC RAISE AN ERROR?
--------------------------------------------------------------------------------

If conversion does NOT make sense:

    uid="test"

Then Pydantic will raise a ValidationError, because:
- "test" cannot be converted into an integer

--------------------------------------------------------------------------------
WHY THIS BEHAVIOR EXISTS
--------------------------------------------------------------------------------

Real-world data often comes as strings:
- JSON payloads
- Environment variables
- Query parameters
- Form submissions

Pydantic prioritizes:
- Practical correctness
- Developer convenience
- Predictable behavior

Strict validation can be enabled when needed, but coercion is the default.
================================================================================
"""
