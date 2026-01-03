"""
Pydantic Model Configuration, Serialization & Custom JSON Encoding
=================================================================

This example demonstrates:
- Model configuration using `ConfigDict` (Pydantic v2)
- Custom JSON encoders for non-JSON-native types (`datetime`)
- Nested models and default values
- Converting models to Python dicts and JSON strings

Libraries:
----------
pydantic.BaseModel
pydantic.ConfigDict
datetime.datetime
typing.List

Official Documentation:
----------------------
https://docs.pydantic.dev/latest/concepts/serialization/
https://docs.pydantic.dev/latest/concepts/models/#model-config
"""

from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, ValidationError


# ======================================================
# ADDRESS MODEL
# ======================================================

class Address(BaseModel):
    """
    Address model.

    Fields:
    -------
    street : str
        Street name

    city : str
        City name

    zipcode : str
        Postal / ZIP code
    """
    street: str
    city: str
    zipcode: str


# ======================================================
# USER MODEL WITH CONFIGURATION
# ======================================================

class User(BaseModel):
    """
    User model demonstrating advanced serialization.

    Fields:
    -------
    id : int
        Unique user identifier

    name : str
        Full name

    email : str
        Email address

    is_active : bool, optional
        Account status (default: True)

    createdAt : datetime
        Account creation timestamp

    address : Address
        Nested Address model

    tags : List[str], optional
        User tags (default: empty list)

    Model Configuration:
    --------------------
    - Custom JSON encoder for datetime objects
    """

    id: int
    name: str
    email: str
    is_active: bool = True
    createdAt: datetime
    address: Address
    tags: List[str] = []

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime('%d-%m-%Y %H:%M:%S')
        }
    )


# ======================================================
# MODEL INSTANTIATION
# ======================================================

try:
    user = User(
        id=1,
        name="John Cena",
        email="johncena@cantseeme.com",
        is_active=True,
        createdAt=datetime(2024, 3, 15, 14, 30),
        address=Address(
            street="Kingsland",
            city="Madagascar",
            zipcode="380001"
        ),
        tags=["premium", "subscriber"]
    )

    # Convert model to Python dictionary
    python_dict = user.model_dump()
    print("Python Dictionary Output:")
    print(python_dict)

    # Convert model to JSON string (uses custom encoder)
    json_str = user.model_dump_json()
    print("\nJSON Output:")
    print(json_str)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Invalid field values are provided
    - Nested model validation fails
    - Type coercion errors occur
    """
    print("\nValidation Error Occurred:")
    print(e)
