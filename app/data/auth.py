import bcrypt
from app.data.db import connect_database 


# turns a normal password into a secure hashed password
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")

# checks if the entered password matches the saved hashed password
def verify_password(plain_text_password, hashed_password):
    check_password = bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))
    return check_password

# registers a new user if the username is not already taken
def register_user(username, password,role):
    conn = connect_database()
    cursor = conn.cursor()

    # check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Username already exists")
        conn.close()
        return False

    # hash the password
    hashed_password = hash_password(password)

    # insert into the database
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hashed_password, role)
    )
    conn.commit()
    conn.close()
    print("User registered successfully!")
    return True

# checks if a username already exists in the file
def user_exist(username): 
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone() 
    conn.close()
    return user
# logs in the user by checking username and verifying the password
def login_user(username, password):
    conn = connect_database()
    cursor = conn.cursor()

    # find user in database
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        hashed_password = row[0]
        if verify_password(password, hashed_password):
            print("Login successful")
            return True
        else:
            print("Incorrect password")
            return False
    else:
        print("Username not found")
        return False

# checks if the username follows the required rules
def validate_username(username):
    if len(username) >= 4 and username.isalnum():
        return (True,"")
    else:
        return(False,"Username must be atleast 4 characters long and must only contain alphabet and numbers ")

# checks if the password follows all safety rules
def validate_password(password):
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long.")
    if not any(c.isupper() for c in password):
        return (False, "Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        return (False, "Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        return (False, "Password must contain at least one number.")
    return (True, "")
