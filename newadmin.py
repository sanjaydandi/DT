import bcrypt
import pandas as pd
import os

credentials_file = "data/credentials.csv"
os.makedirs("data", exist_ok=True)

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Create initial admin credentials
data = {
    "Username": ["admin"],
    "Password": [hash_password("admin123")],  # Default admin password
    "Role": ["admin"]
}

df = pd.DataFrame(data)
df.to_csv(credentials_file, index=False)
print("Admin user created successfully!")
