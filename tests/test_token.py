from app.core.security import create_token

token = create_token(
    "employee@test.com",
    "employee",
)


assert token is not None
print(token)
