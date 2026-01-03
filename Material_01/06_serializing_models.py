"""
================================================================================
PYDANTIC — SERIALIZING MODELS (DICT & JSON)
================================================================================

This example demonstrates how to:
- Create a validated Pydantic model
- Convert the model into a Python dictionary
- Serialize the model into JSON

Key concept:
Pydantic models provide built-in serialization methods that make it easy
to move between Python objects and JSON-compatible representations.
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
# MODEL CREATION & SERIALIZATION
# ==============================================================================

try:
    user = User(
        uid=101,
        username="jamesbond007",
        email="jamesbond@007.com",
        age=40,
    )

    # --------------------------------------------------------------------------
    # PRINTING THE MODEL
    # --------------------------------------------------------------------------
    # Shows the full validated state of the model
    print(user)
    # uid=101 username='jamesbond007' email='jamesbond@007.com'
    # age=40 bio='' is_active=True fullname=None createdAt=None

    # --------------------------------------------------------------------------
    # CONVERT MODEL TO DICTIONARY
    # --------------------------------------------------------------------------
    # model_dump() returns a standard Python dict
    print(user.model_dump())
    # {
    #   'uid': 101,
    #   'username': 'jamesbond007',
    #   'email': 'jamesbond@007.com',
    #   'age': 40,
    #   'bio': '',
    #   'is_active': True,
    #   'fullname': None,
    #   'createdAt': None
    # }

    # --------------------------------------------------------------------------
    # CONVERT MODEL TO JSON (COMPACT)
    # --------------------------------------------------------------------------
    # model_dump_json() returns a JSON string
    print(user.model_dump_json())
    # {"uid":101,"username":"jamesbond007","email":"jamesbond@007.com",
    #  "age":40,"bio":"","is_active":true,"fullname":null,"createdAt":null}

    # --------------------------------------------------------------------------
    # CONVERT MODEL TO JSON (PRETTY PRINTED)
    # --------------------------------------------------------------------------
    # JSON output with indentation for readability
    print(user.model_dump_json(indent=2))
    # {
    #   "uid": 101,
    #   "username": "jamesbond007",
    #   "email": "jamesbond@007.com",
    #   "age": 40,
    #   "bio": "",
    #   "is_active": true,
    #   "fullname": null,
    #   "createdAt": null
    # }

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
Key Takeaways
--------------------------------------------------------------------------------

- model_dump() converts a Pydantic model into a Python dict
- model_dump_json() converts the model into a JSON string
- JSON output can be formatted using indentation
- Serialization preserves validated data and types

These methods are commonly used when:
- Returning API responses (FastAPI)
- Storing data in JSON-based systems
- Logging or debugging structured data
================================================================================
"""
