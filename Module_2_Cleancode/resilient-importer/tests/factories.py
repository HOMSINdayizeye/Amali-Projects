from resilient_importer.models import User


def make_user(**kwargs) -> User:
    """Create a User instance with sensible defaults."""
    defaults = {
        "user_id": "1",
        "name": "Alice",
        "email": "alice@example.com",
    }
    defaults.update(kwargs)
    return User(**defaults)
