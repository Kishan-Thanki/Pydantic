"""
================================================================================
PYDANTIC — MODEL VALIDATORS (CROSS-FIELD VALIDATION)
================================================================================

This example demonstrates **model-level validation** using Pydantic v2.

So far, we validated:
- Individual fields (using `field_validator`)
- Types, constraints, and formats

Now we move to a more advanced and very common requirement:

**Validating relationships between multiple fields**

Typical real-world use cases:
- Password & confirm-password matching
- Date ranges (start_date < end_date)
- Conditional rules (field A required if field B is set)

For this, Pydantic provides `model_validator`.
"""

from pydantic import (
    BaseModel,
    EmailStr,
    ValidationError,
    model_validator,
)

# ==============================================================================
# USER REGISTRATION MODEL
# ==============================================================================

class UserRegistration(BaseModel):
    """
    User registration schema.

    This model validates:
    - Email format
    - Password presence
    - Password confirmation consistency
    """

    email: EmailStr
    password: str
    confirm_password: str

    # --------------------------------------------------------------------------
    # MODEL VALIDATOR (CROSS-FIELD VALIDATION)
    # --------------------------------------------------------------------------

    @model_validator(mode="after")
    def passwords_match(self) -> "UserRegistration":
        """
        Ensures that password and confirm_password are identical.

        Why `mode="after"`?
        - All fields are already individually validated
        - We can safely compare their values
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


# ==============================================================================
# VALIDATION EXAMPLES
# ==============================================================================

# ------------------------------------------------------------------------------
# CASE 1: INVALID REGISTRATION (PASSWORDS DO NOT MATCH)
# ------------------------------------------------------------------------------
try:
    user_invalid = UserRegistration(
        email="jamesbond@007.com",
        password="TopSecret007",
        confirm_password="WrongPassword",
    )

except ValidationError as e:
    print("Validation Error (Passwords mismatch):")
    print(e)


# ------------------------------------------------------------------------------
# CASE 2: VALID REGISTRATION
# ------------------------------------------------------------------------------
try:
    user_valid = UserRegistration(
        email="jamesbond@007.com",
        password="TopSecret007",
        confirm_password="TopSecret007",
    )

    print("User registration successful:")
    print(user_valid)

except ValidationError as e:
    print("Validation Error:")
    print(e)


"""
--------------------------------------------------------------------------------
KEY TAKEAWAYS
--------------------------------------------------------------------------------

1. `model_validator` is used for **cross-field validation**
2. `mode="after"` runs AFTER all field-level validation
3. Perfect for:
   - Password confirmation
   - Interdependent fields
   - Business rules
4. Keeps validation logic centralized and explicit
5. Prevents invalid state from ever entering your system

This is the final layer of validation:
✔ Field-level correctness
✔ Model-level consistency
================================================================================
"""
