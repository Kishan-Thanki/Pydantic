"""
Pydantic Models: Cart & BlogPost
===============================

This example demonstrates:
- Using collection types (List, Dict)
- Optional fields with default values
- Nested and structured data validation
- Automatic type coercion and error handling

Libraries:
----------
pydantic.BaseModel
typing (List, Dict, Optional)

Official Documentation:
----------------------
https://docs.pydantic.dev/
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, ValidationError


class Cart(BaseModel):
    """
    Shopping Cart model.

    Fields:
    -------
    user_id : int
        Unique identifier for the user.
        - Converts numeric strings to int

    items : List[str]
        List of product names in the cart.
        - Must be a list
        - Each item must be a string

    quantities : Dict[str, int]
        Mapping of product name → quantity.
        - Keys must be strings
        - Values must be integers
        - Numeric strings are converted to int
    """
    user_id: int
    items: List[str]
    quantities: Dict[str, int]


class BlogPost(BaseModel):
    """
    Blog post model.

    Fields:
    -------
    title : str
        Title of the blog post.
        - Required field

    content : str
        Main body/content of the blog post.
        - Required field

    tags : Optional[str], optional
        Tags associated with the blog post.
        - Defaults to "#blogs" if not provided
        - Can be explicitly set to None
    """
    title: str
    content: str
    tags: Optional[str] = "#blogs"


# ==========================
# INPUT DATA EXAMPLES
# ==========================

# ✔ Valid Cart data
# cart_data = {
#     "user_id": "101",
#     "items": ["Laptop", "Mouse"],
#     "quantities": {"Laptop": 1, "Mouse": "2"}
# }

# ❌ Invalid Cart: quantity must be int
# cart_data = {
#     "user_id": 102,
#     "items": ["Keyboard"],
#     "quantities": {"Keyboard": "two"}
# }

# ✔ Valid BlogPost with default tag
# blog_data = {
#     "title": "Pydantic Basics",
#     "content": "Pydantic makes data validation easy."
# }

# ✔ Valid BlogPost with custom tag
# blog_data = {
#     "title": "Advanced Typing",
#     "content": "Using List, Dict, Optional in Pydantic.",
#     "tags": "#python #typing"
# }

# ❌ Invalid BlogPost: title missing
cart_data = {
    "user_id": 103,
    "items": ["Book"],
    "quantities": {"Book": 1}
}

blog_data = {
    "content": "This post has no title."
}


# ==========================
# MODEL INSTANTIATION
# ==========================

try:
    cart = Cart(**cart_data)
    print("Validated Cart Object:")
    print(cart)

    blog = BlogPost(**blog_data)
    print("\nValidated BlogPost Object:")
    print(blog)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Required fields are missing
    - Incorrect collection types are provided
    - Type coercion fails

    Errors are detailed and easy to debug.
    """
    print("\nValidation Error Occurred:")
    print(e)
