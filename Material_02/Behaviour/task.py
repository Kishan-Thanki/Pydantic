"""
Pydantic Booking Model with Constraints & Computed Field
=======================================================

This example demonstrates:
- Field constraints using `Field`
- Numeric validation (`ge=1`)
- Computed/derived fields using `@computed_field`
- Clean and API-ready data modeling

Library:
--------
pydantic (v2+)

Official Documentation:
----------------------
https://docs.pydantic.dev/latest/concepts/fields/
https://docs.pydantic.dev/latest/concepts/fields/#computed-fields
"""

from pydantic import BaseModel, Field, computed_field, ValidationError


class Booking(BaseModel):
    """
    Booking model definition.

    Fields:
    -------
    user_id : int
        Unique identifier of the user making the booking.

    room_id : int
        Unique identifier of the room being booked.

    nights : int
        Number of nights for the stay.
        - Must be >= 1

    rate_per_night : float
        Cost per night.
        - Accepts int, float, or numeric strings

    Computed Fields:
    ----------------
    total_amount : float
        Total booking cost.
        - Calculated as nights * rate_per_night
        - Not provided in input
        - Automatically included in output
    """

    user_id: int
    room_id: int
    nights: int = Field(..., ge=1, description="Number of nights (minimum 1)")
    rate_per_night: float

    @computed_field
    @property
    def total_amount(self) -> float:
        """
        Calculate total booking amount dynamically.
        """
        return self.nights * self.rate_per_night


# ==========================
# INPUT DATA EXAMPLES
# ==========================

# ✔ Valid booking
# booking_data = {
#     "user_id": 101,
#     "room_id": 202,
#     "nights": 3,
#     "rate_per_night": 2500.50
# }

# ✔ Valid with type coercion
# booking_data = {
#     "user_id": "102",
#     "room_id": "203",
#     "nights": "2",
#     "rate_per_night": "1999.99"
# }

# ❌ Invalid: nights < 1
# booking_data = {
#     "user_id": 103,
#     "room_id": 204,
#     "nights": 0,
#     "rate_per_night": 1800
# }

# ❌ Invalid: missing required field
booking_data = {
    "user_id": 104,
    "room_id": 205,
    "nights": 2
}


# ==========================
# MODEL INSTANTIATION
# ==========================

try:
    booking = Booking(**booking_data)
    print("Validated Booking Object:")
    print(booking)

    print("\nAccessing individual fields:")
    print("User ID:", booking.user_id)
    print("Room ID:", booking.room_id)
    print("Nights:", booking.nights)
    print("Rate/Night:", booking.rate_per_night)
    print("Total Amount:", booking.total_amount)

except ValidationError as e:
    """
    ValidationError:
    ----------------
    Raised when:
    - Required fields are missing
    - Field constraints are violated
    - Type conversion fails

    Error messages are structured and API-friendly.
    """
    print("\nValidation Error Occurred:")
    print(e)
