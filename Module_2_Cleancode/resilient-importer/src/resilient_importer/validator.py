"""User data validation.

Provides business-rule validation for User objects, ensuring required
fields are present and that email addresses conform to a basic format.
"""

import re
from dataclasses import dataclass
from typing import List

from .models import User


@dataclass
class ValidationResult:
    """Stores the result of a validation check.

    Attributes:
        is_valid: True when the user passes all validation rules.
        errors: A list of human-readable validation error messages.
    """

    is_valid: bool
    errors: List[str]


class UserValidator:
    """Validates User data against business rules.

    Rules enforced:
    - ``user_id`` must not be empty.
    - ``name`` must not be empty.
    - ``email`` must match a basic RFC-like regex.
    """

    EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def validate(self, user: User) -> ValidationResult:
        """Validate a user object and return a ValidationResult.

        Args:
            user: The User instance to validate.

        Returns:
            A ValidationResult indicating whether the user is valid
            and collecting any error messages.
        """
        errors: List[str] = []

        if not user.user_id:
            errors.append("user_id must not be empty")
        if not user.name:
            errors.append("name must not be empty")
        if not user.email or not self.EMAIL_REGEX.match(user.email):
            errors.append(f"Invalid email address: {user.email}")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
