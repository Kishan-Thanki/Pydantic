"""
Pydantic Employee Model with Field Constraints
=============================================

This example demonstrates:
- Field-level validation using `Field`
- String length constraints
- Numeric value constraints
- Optional fields with default values
- Clear, descriptive schema metadata

Libraries:
----------
pydantic.BaseModel
pydantic.Field
typing.Optional

Official Documentation:
----------------------
https://docs.pydantic.dev/usage/models/
https://docs.pydantic.dev/usage/schema/
"""

from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class Employee(BaseModel):
    """
    Employee model definition.

    Fields:
    -------
    id : int
        Unique identifier for the employee.
        - Accepts integers
        - Converts numeric strings to int

    name : str
        Employee name.
        - Minimum length: 3 characters
        - Maximum length: 50 characters
        - Required field

    department : Optional[str], optional
        Department name.
        - Defaults to "General" if not provided
        - Can be explicitly set to None

    salary : float
        Employee salary.
        - Must be >= 10000
        - Accepts int, float, or numeric strings
    """

    id: int

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee Name",
        examples=["John Cena"]
    )

    department: Optional[str] = "General"

    salary: float = Field(
        ...,
        ge=10000,
        description="Employee Salary (minimum 10000)"
    )


# ==========================
# INPUT DATA EXAMPLES
# ==========================

# ✔ Valid employee
# employee_data = {
#     "id": 1,
#     "name": "John Cena",
#     "department": "HR",
#     "salary": 50000
# }

# ✔ Valid employee with default department
# employee_data = {
#     "id": "2",
#     "name": "Alice",
#     "salary": "25000"
# }

# ❌ Invalid: name too short
# employee_data = {
#     "id": 3,
#     "name": "Al",
#     "salary": 20000
# }

# ❌ Invalid: salary below minimum
# employee_data = {
#     "id": 4,
#     "name": "Robert",
#     "salary": 8000
# }

# ❌ Invalid: missing required salary
employee_data = {
    "id": 5,
    "name": "Michael Scott"
}


# ==========================
# MODEL INSTANTIATION
# ==========================

try:
    employee = Employee(**employee_data)
    print("Validated Employee Object:")
    print(employee)

    print("\nAccessing individual fields:")
    print("ID:", employee.id)
    print("Name:", employee.name)
    print("Department:", employee.department)
    print("Salary:", employee.salary)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Required fields are missing
    - Field constraints are violated
    - Type coercion fails

    Errors are detailed and ideal for API responses.
    """
    print("\nValidation Error Occurred:")
    print(e)
