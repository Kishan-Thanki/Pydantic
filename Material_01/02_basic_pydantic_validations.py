"""
================================================================================
THE PYDANTIC WAY — CLEAN & RELIABLE DATA VALIDATION
================================================================================

Purpose of this example:
- Show how Pydantic replaces manual validation
- Demonstrate single-pass validation with clear errors
- Highlight schema-based data correctness

Key idea:
Define a schema → pass data → get either a validated object or a ValidationError
"""

from pydantic import BaseModel, ValidationError

# ==============================================================================
# SCHEMA DEFINITION
# ==============================================================================

class User(BaseModel):
    """
    User schema.

    Validation rules are inferred directly from type hints.
    No manual checks or custom error handling required.
    """
    username: str
    email: str
    age: int


# ==============================================================================
# VALID INPUT
# ==============================================================================

try:
    user = User(
        username="JamesBond007",
        email="jamesbond@007.com",
        age=40,
    )
    print(user)

except ValidationError as e:
    print(e)


# ==============================================================================
# INVALID INPUT (MULTIPLE ERRORS IN ONE PASS)
# ==============================================================================

try:
    user = User(
        username="JohnCena",
        email=None,   # invalid
        age="WWE",    # invalid
    )
    print(user)

except ValidationError as e:
    print("\nValidation Errors:")
    print(e)

# ==============================================================================
# EXAMPLE ERROR OUTPUT
# ==============================================================================

"""
Pydantic Validation Errors:
2 validation errors for User

email
    Input should be a valid string
    [type=string_type, input_value=None, input_type=NoneType]

age
    Input should be a valid integer, unable to parse string as an integer
    [type=int_parsing, input_value='WWE', input_type=str]

"""

"""
--------------------------------------------------------------------------------
OBSERVED BEHAVIOR
--------------------------------------------------------------------------------

- Validation occurs at object creation
- All invalid fields are detected together
- Errors are structured and human-readable
- Business logic remains untouched

--------------------------------------------------------------------------------
WHY THIS MATTERS
--------------------------------------------------------------------------------

Pydantic provides:
- Schema-first data validation
- Automatic type enforcement
- Predictable error reporting

This makes it ideal for:
- API request/response models (FastAPI)
- Configuration schemas
- Data pipelines
- AI / agent input-output contracts
================================================================================
"""