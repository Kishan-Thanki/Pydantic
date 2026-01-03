"""
================================================================================
PYDANTIC — REQUIRED FIELDS vs DEFAULT & OPTIONAL FIELDS
================================================================================

This example demonstrates how Pydantic treats:
- Required fields
- Fields with default values
- Optional (nullable) fields

Core rules illustrated:
1. Fields WITHOUT default values are REQUIRED
2. Fields WITH default values are OPTIONAL
3. Optional fields may explicitly accept None
4. Missing optional/default fields do NOT raise validation errors
"""

from datetime import datetime

from pydantic import BaseModel, ValidationError

# ==============================================================================
# SCHEMA DEFINITION
# ==============================================================================

class User(BaseModel):
    """
    User schema illustrating required, default, and optional fields.

    Field categories:
    - Required fields:
        • uid
        • username
        • email
        • age

    - Fields with default values:
        • bio
        • is_active

    - Optional (nullable) fields:
        • fullname
        • createdAt
    """

    # ---------------------------
    # REQUIRED FIELDS
    # ---------------------------
    uid: int
    username: str
    email: str
    age: int

    # ---------------------------
    # DEFAULT VALUE FIELDS
    # ---------------------------
    bio: str = ""
    is_active: bool = True

    # ---------------------------
    # OPTIONAL (NULLABLE) FIELDS
    # ---------------------------
    
    """
    Python version note:
    - `str | None` syntax requires Python 3.10+
    - For Python < 3.10, use `Optional[str]` instead
    """

    fullname: str | None = None
    createdAt: datetime | None = None



# ==============================================================================
# CASE 1: NO INPUT DATA PROVIDED
# ==============================================================================

"""
Attempting to create a User without any input data.

Expected behavior:
- Pydantic raises a ValidationError
- ONLY required fields appear in the error output
- Fields with defaults or optional fields are ignored
"""

try:
    user1 = User()
    print(user1)

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
EXPECTED ERROR (ABBREVIATED):

4 validation errors for User
uid
  Field required
username
  Field required
email
  Field required
age
  Field required

Note:
- bio, is_active, fullname, createdAt do NOT appear
"""


# ==============================================================================
# CASE 2: ONLY REQUIRED FIELDS PROVIDED
# ==============================================================================

"""
Providing values for all required fields only.

Expected behavior:
- Object is created successfully
- Default values are automatically populated
- Optional fields default to None
"""

try:
    user2 = User(
        uid=101,
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

uid=101
username='jamesbond007'
email='jamesbond@007.com'
age=40
bio=''
is_active=True
fullname=None
createdAt=None

--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

- Required fields must be provided
- Default fields are auto-filled when missing
- Optional fields accept None safely
- Validation remains strict for required data
- No manual checks or fallback logic needed

This behavior is fundamental to how Pydantic models real-world data:
clear requirements, sensible defaults, and predictable structure.
================================================================================
"""
