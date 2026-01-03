"""
================================================================================
PYDANTIC — MODEL VALIDATORS (BEST PRACTICES)
================================================================================
"""

from pydantic import (
    BaseModel,
    EmailStr,
    ValidationError,
    model_validator,
)


class UserRegistration(BaseModel):

    email: EmailStr
    password: str
    confirm_password: str

    # --------------------------------------------------------------------------
    # MODEL VALIDATOR (CROSS-FIELD VALIDATION)
    # --------------------------------------------------------------------------

    @model_validator(mode="after")
    def passwords_match(self) -> "UserRegistration":
        """
        Ensure password and confirm_password are identical.

        Best practices followed here:
        1. Always return `self` (even if not modified)
        2. Either return the model OR raise an error
        3. Raise ValueError (Pydantic converts it to ValidationError)
        4. Do NOT mutate data before raising errors
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self


try:
    user_invalid = UserRegistration(
        email="jamesbond@007.com",
        password="TopSecret007",
        confirm_password="WrongPassword",
    )

except ValidationError as e:
    print("Validation Error (Passwords mismatch):")
    print(e)


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

1. Use `model_validator` for cross-field validation
2. Prefer `mode="after"` when comparing validated fields
3. Always return the model instance (`self`)
4. Raise `ValueError` — Pydantic wraps it as `ValidationError`
5. Never partially mutate data before raising errors

Following these rules keeps validation:
Predictable
Maintainable
Production-safe

This pattern is essential for real-world forms, APIs, and workflows.
================================================================================
"""
