"""
Pydantic Product Model Documentation
===================================

This task demonstrates how to define a **Product model** using
Pydantic's BaseModel with:
- Required and optional fields
- Default values
- Automatic type conversion
- Validation behavior

Library:
---------
pydantic.BaseModel

Official Documentation:
-----------------------
https://docs.pydantic.dev/
"""

from pydantic import BaseModel, ValidationError


class Product(BaseModel):
    """
    Product model definition.

    Fields:
    -------
    id : int
        Unique identifier for the product.
        - Accepts integers
        - Converts numeric strings (e.g., "201") to int
        - Fails for invalid values (e.g., "20A")

    name : str
        Name of the product.
        - Must be a string

    price : float
        Price of the product.
        - Accepts float or int values
        - Converts numeric strings (e.g., "99.99")
        - Fails for non-numeric strings

    in_stock : bool, optional
        Availability status of the product.
        - Defaults to True
        - Accepts True/False
        - Converts truthy strings ("true", "1", "yes")
    """
    id: int
    name: str
    price: float
    in_stock: bool = True


# ==========================
# INPUT DATA VARIATIONS
# ==========================

# ✔ Valid: exact types
# input_data = {"id": 1, "name": "Laptop", "price": 79999.99, "in_stock": True}

# ✔ Valid: auto type conversion
# input_data = {"id": "2", "name": "Mouse", "price": "499.50", "in_stock": "true"}

# ✔ Valid: default value used for in_stock
# input_data = {"id": 3, "name": "Keyboard", "price": 1499.00}

# ❌ Invalid: price cannot be converted to float
# input_data = {"id": 4, "name": "Monitor", "price": "free"}

# ❌ Invalid: id cannot be converted to int
# input_data = {"id": "10X", "name": "USB Cable", "price": 199}

# ❌ Invalid: invalid boolean string
input_data = {"id": 5, "name": "Headphones", "price": 2999, "in_stock": "maybe"}


# ==========================
# MODEL INSTANTIATION
# ==========================

try:
    product = Product(**input_data)
    print("Validated Product Object:")
    print(product)

    # Accessing individual fields
    print("\nAccessing individual fields:")
    print("ID:", product.id)
    print("Name:", product.name)
    print("Price:", product.price)
    print("In Stock:", product.in_stock)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Required fields are missing
    - Type conversion fails
    - Invalid values are provided

    Error output is structured and developer-friendly.
    """
    print("Validation Error Occurred:")
    print(e)
