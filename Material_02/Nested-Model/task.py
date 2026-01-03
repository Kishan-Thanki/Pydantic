"""
Hierarchical / Deeply Nested Pydantic Models
===========================================

This example demonstrates:
- Multi-level nested models (Course → Modules → Lessons)
- Using lists of nested objects
- Forward references in type hints
- Clean, scalable data modeling for complex schemas

Libraries:
----------
pydantic.BaseModel
typing.List

Official Documentation:
----------------------
https://docs.pydantic.dev/latest/concepts/models/#nested-models
"""

from typing import List
from pydantic import BaseModel, ValidationError


# ======================================================
# LESSON MODEL — LEAF NODE
# ======================================================

class Lesson(BaseModel):
    """
    Lesson model.

    Fields:
    -------
    lesson_id : int
        Unique identifier for the lesson

    topic : str
        Topic covered in the lesson
    """
    lesson_id: int
    topic: str


# ======================================================
# MODULE MODEL — CONTAINS LESSONS
# ======================================================

class Module(BaseModel):
    """
    Module model.

    Fields:
    -------
    module_id : int
        Unique identifier for the module

    name : str
        Name of the module

    lessons : List[Lesson]
        List of lessons under this module
    """
    module_id: int
    name: str
    lessons: List["Lesson"]


# ======================================================
# COURSE MODEL — TOP LEVEL
# ======================================================

class Course(BaseModel):
    """
    Course model.

    Fields:
    -------
    course_id : int
        Unique identifier for the course

    title : str
        Course title

    modules : List[Module]
        List of modules included in the course
    """
    course_id: int
    title: str
    modules: List["Module"]


# Resolve forward references (required in Pydantic v2)
Module.model_rebuild()
Course.model_rebuild()


# ======================================================
# USAGE EXAMPLE
# ======================================================

try:
    course_data = {
        "course_id": 101,
        "title": "Python with Pydantic",
        "modules": [
            {
                "module_id": 1,
                "name": "Basics",
                "lessons": [
                    {"lesson_id": 1, "topic": "Introduction"},
                    {"lesson_id": 2, "topic": "Data Types"}
                ]
            },
            {
                "module_id": 2,
                "name": "Advanced",
                "lessons": [
                    {"lesson_id": 3, "topic": "Validators"},
                    {"lesson_id": 4, "topic": "Nested Models"}
                ]
            }
        ]
    }

    course = Course(**course_data)

    print("Validated Course Object:")
    print(course)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Nested structures are invalid
    - Required fields are missing
    - Type mismatches occur
    """
    print("\nValidation Error Occurred:")
    print(e)
