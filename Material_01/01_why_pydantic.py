"""
================================================================================
PYDANTIC — INTRODUCTION & MOTIVATION (VERBOSE, DOCUMENTED)
================================================================================

Pydantic is one of the most popular **data validation and parsing libraries**
in the Python ecosystem.

Its primary purpose is to ensure that **incoming data strictly matches the
shape, type, and constraints we expect** in our application.

--------------------------------------------------------------------------------
WHERE PYDANTIC IS USED
--------------------------------------------------------------------------------

Pydantic is widely used in:

- API input/output validation (FastAPI uses Pydantic internally)
- Data processing pipelines
- Configuration management
- AI / ML tooling
- Agent frameworks (e.g., pydantic-ai)
- Any system where **data correctness matters**

In short:
Whenever you want to be confident that your data is *exactly* what you expect,
**Pydantic is the go-to solution**.

--------------------------------------------------------------------------------
WHY PYDANTIC WORKS SO WELL
--------------------------------------------------------------------------------

- Uses Python **type hints** for validation
- Automatically converts compatible types
- Collects **all validation errors at once**
- Works cleanly with nested objects, lists, and dictionaries
- Reduces boilerplate code
- Produces readable, structured error messages

--------------------------------------------------------------------------------
WHY NOT JUST DO MANUAL VALIDATION?
--------------------------------------------------------------------------------

Yes, we *can* manually validate data using plain Python.

But this approach quickly becomes:
- Verbose
- Hard to maintain
- Error-prone
- Difficult to scale for complex data structures

Below is an example of **manual validation** to demonstrate the problem.
"""

# ==============================================================================
# MANUAL DATA VALIDATION (WITHOUT PYDANTIC)
# ==============================================================================

def create_user(username, email, age):
    """
    Manually validates input data before creating a user.

    Problems with this approach:
    - Validation logic is tightly coupled with business logic
    - Only the FIRST error is reported
    - Adding more fields increases complexity exponentially
    - Nested objects, lists, and custom rules become very hard to manage
    """
    try:
        if not isinstance(username, str):
            raise TypeError(f"Username {username} must be a string")

        if not isinstance(email, str):
            raise TypeError(f"Email {email} must be a string")

        if not isinstance(age, int):
            raise TypeError(f"Age {age} must be an integer")

        user_context = {
            "Username": username,
            "Email": email,
            "Age": age,
        }

        return f"User {user_context} created successfully!"

    except Exception as e:
        print(f"Error: {e}")


# ------------------------------------------------------------------------------
# VALID INPUT
# ------------------------------------------------------------------------------

user1 = create_user("JamesBond007", "jamesbond@007.com", 40)
if user1:
    print(user1)


# ------------------------------------------------------------------------------
# INVALID INPUT
# ------------------------------------------------------------------------------

user2 = create_user("JohnCena", None, "WWE")
if user2:
    print(user2)

"""
--------------------------------------------------------------------------------
PROBLEMS WITH THE MANUAL APPROACH
--------------------------------------------------------------------------------

1. Multiple validation errors exist in `user2`, but only ONE is reported.
2. You must fix errors one-by-one and rerun the program repeatedly.
3. Validation code quickly becomes cluttered and hard to read.
4. Scaling this approach to:
   - Lists
   - Dictionaries
   - Nested objects
   - Custom rules
   - Conditional validation
   becomes painful and error-prone.

Now imagine doing this for:
- API request bodies
- Database models
- Configuration files
- AI prompt schemas

This is exactly where **Pydantic shines**.
"""