"""
================================================================================
PYDANTIC — REQUIRED FIELDS & RUNTIME VALIDATION
================================================================================

Core concept demonstrated here:
- Fields WITHOUT default values are **required**
- Validation happens at **object creation**
- Missing required fields raise a `ValidationError`
- ALL missing fields are reported at once
"""

from pydantic import BaseModel, ValidationError

# ==============================================================================
# MODEL DEFINITION
# ==============================================================================

class User(BaseModel):
    """
    User schema defined using Pydantic.

    Rules:
    - All fields are REQUIRED
    - Requirement is inferred from:
        • type annotation
        • absence of a default value
    """
    username: str
    email: str
    age: int


# ==============================================================================
# CASE 1: NO DATA PROVIDED → VALIDATION ERROR
# ==============================================================================

try:
    user1 = User()   # No input data
    print(user1)

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
EXPECTED OUTPUT:

Error: 3 validation errors for User
username
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.5/v/missing
email
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.5/v/missing
age
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.5/v/missing

Key point:
- Pydantic reports ALL missing required fields together
"""


# ==============================================================================
# CASE 2: ALL REQUIRED DATA PROVIDED → SUCCESS
# ==============================================================================

try:
    user2 = User(
        username="jamesbond007",
        email="jamesbond@007.com",
        age=40,
    )
    print(user2)

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
OUTPUT:

username='jamesbond007' email='jamesbond@007.com' age=40

--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

- Required fields are enforced automatically
- Validation happens at instantiation time
- No manual checks or boilerplate code
- BaseModel provides:
    • automatic __init__
    • automatic validation
    • readable object representation

This behavior scales naturally to:
- Nested models
- Lists and dictionaries
- Optional fields
- API schemas (FastAPI)
================================================================================
"""
