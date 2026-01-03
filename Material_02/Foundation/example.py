"""
Pydantic Model Documentation & Validation Walkthrough
=====================================================

This example demonstrates how **Pydantic's BaseModel**:
- Performs **data validation**
- Applies **type coercion (when possible)**
- Raises **clear validation errors** when data is invalid

Library:
---------
pydantic.BaseModel is commonly used in:
- FastAPI
- Data validation layers
- Configuration management
- API request/response schemas

Official Docs:
--------------
https://docs.pydantic.dev/
"""

from pydantic import BaseModel, ValidationError


class User(BaseModel):
    """
    User model definition.

    Fields:
    -------
    id : int
        Unique identifier for the user.
        - Accepts integers
        - Will attempt to convert string numbers (e.g., "101")
        - Fails if conversion is not possible (e.g., "101a")

    username : str
        Username of the user.
        - Must be a string

    is_active : bool
        Indicates whether the user is active.
        - Accepts booleans (True / False)
        - Accepts truthy strings like "true", "True", "1"
        - Rejects invalid strings like "Saach"
    """
    id: int
    username: str
    is_active: bool


# ==========================
# INPUT DATA VARIATIONS
# ==========================

# ✔ Valid: perfect match
# input_data = {'id': 101, 'username': 'johncena', 'is_active': True}

# ❌ Invalid: field name mismatch (isactive != is_active)
# input_data = {'id': 101, 'username': 'johncena', 'isactive': True}

# ✔ Valid: string "True" → coerced to boolean True
# input_data = {'id': 101, 'username': 'johncena', 'is_active': 'True'}

# ❌ Invalid: "Saach" cannot be converted to boolean
# input_data = {'id': 101, 'username': 'johncena', 'is_active': 'Saach'}

# ✔ Valid: string "101" → coerced to integer 101
# input_data = {'id': '101', 'username': 'johncena', 'is_active': 'True'}

# ❌ Invalid: "101a" cannot be converted to integer
input_data = {'id': '101a', 'username': 'johncena', 'is_active': 'True'}


# ==========================
# MODEL INSTANTIATION
# ==========================

try:
    user = User(**input_data)
    print("Validated User Object:")
    print(user)

    # Accessing fields
    print("\nAccessing individual fields:")
    print("ID:", user.id)
    print("Username:", user.username)
    print("Is Active:", user.is_active)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Required fields are missing
    - Field names do not match
    - Type coercion fails
    - Values are invalid

    Error output is structured and machine-readable.
    """
    print("Validation Error Occurred:")
    print(e)
