from app.security import hash_password, verify_password

h1 = hash_password("secret123")
h2 = hash_password("secret123")

print(h1 == h2)                                      # False
print(verify_password("secret123", h1)) # True
print(verify_password("wrong",h1))      # False