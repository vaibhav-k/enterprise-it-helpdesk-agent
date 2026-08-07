from app.database.users import (
    get_user,
    verify_password,
)

user = get_user("employee@test.com")


if user:

    assert user.username == "employee@test.com"
    assert user.role == "employee"
    assert verify_password(
        "Password123!",
        user.password_hash,
    )
