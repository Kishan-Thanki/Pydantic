"""
Advanced Pydantic Validation & Computed Fields
=============================================

This example demonstrates **Pydantic v2 features**:
- Field-level validation using `@field_validator`
- Model-level validation using `@model_validator`
- Derived/computed fields using `@computed_field`

Library:
--------
pydantic (v2+)

Official Documentation:
----------------------
https://docs.pydantic.dev/latest/concepts/validators/
https://docs.pydantic.dev/latest/concepts/fields/#computed-fields
"""

from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
    computed_field,
    ValidationError,
)


# ======================================================
# USER MODEL — FIELD VALIDATION
# ======================================================

class User(BaseModel):
    """
    User model with custom field validation.

    Fields:
    -------
    username : str
        Username of the user.
        - Must be at least 4 characters long
    """
    username: str

    @field_validator('username')
    @classmethod
    def username_length(cls, v: str) -> str:
        """
        Field-level validator for `username`.

        Runs automatically whenever `username` is set.
        Raises an error if the length is less than 4.
        """
        if len(v) < 4:
            raise ValueError("Username must be at least 4 characters")
        return v


# ======================================================
# SIGNUP MODEL — MODEL VALIDATION
# ======================================================

class SignUpData(BaseModel):
    """
    Signup data model with cross-field validation.

    Fields:
    -------
    password : str
        User password

    confirm_password : str
        Confirmation password
    """
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def password_match(self):
        """
        Model-level validator.

        Runs after all fields are validated.
        Used when validation depends on multiple fields.
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


# ======================================================
# PRODUCT MODEL — COMPUTED FIELD
# ======================================================

class Product(BaseModel):
    """
    Product model with a computed field.

    Fields:
    -------
    price : float
        Price per unit

    quantity : int
        Number of units

    Computed Fields:
    ----------------
    total_price : float
        Automatically calculated as price * quantity
        - Not provided in input
        - Included in output
    """
    price: float
    quantity: int

    @computed_field
    @property
    def total_price(self) -> float:
        """
        Derived field calculated dynamically.
        """
        return self.price * self.quantity


# ======================================================
# USAGE EXAMPLES
# ======================================================

try:
    # ❌ Invalid username (too short)
    # user = User(username="abc")

    # ✔ Valid username
    user = User(username="john_doe")
    print("User:", user)

    # ❌ Password mismatch
    # signup = SignUpData(password="secret123", confirm_password="secret")

    # ✔ Password match
    signup = SignUpData(password="secret123", confirm_password="secret123")
    print("\nSignup Data:", signup)

    # ✔ Computed field example
    product = Product(price=499.99, quantity=3)
    print("\nProduct:", product)
    print("Total Price:", product.total_price)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Field validators fail
    - Model-level validation fails
    - Type coercion fails
    """
    print("\nValidation Error Occurred:")
    print(e)
