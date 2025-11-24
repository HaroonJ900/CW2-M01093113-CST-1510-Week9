import bcrypt

USER_DATA_FILE = "users.txt"
with open(USER_DATA_FILE , 'a') as file:
    pass
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_text_password, hashed_password):
    check_password = bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))
    return check_password

def register_user(username, password):
    with open(USER_DATA_FILE,"r") as file:
        for line in file:
            existing_username = line.strip().split(',')[0]
            if existing_username == username:
                print("Username already exists")
                return False   

    
    hashed_password = hash_password(password)

    with open(USER_DATA_FILE, "a") as file:
        file.write(f'{username},{hashed_password}\n')  
    print("User registered successfully!")


def user_exist(username): 
    with open(USER_DATA_FILE) as file:
        for line in file:
            username_file = line.strip().split(",")[0]
            if username_file == username:
                return True
        else:
            return False
def login_user(username, password):
        with open(USER_DATA_FILE) as file:
            for line in file:
                username_file = line.strip().split(",")[0]
                password_file = line.strip().split(",")[1]
                if username_file == username:
                    if verify_password(password, password_file):
                        print("login successful")
                        return True
                    else:
                        print("incorrect password")
                        return False
                
        print("username was not found")
        return False
        
        

def validate_username(username):
    if len(username) >= 4 and username.isalnum():
        return (True,"")
    else:
        return(False,"Username must be atleast 4 characters long and must only contain alphabet and numbers ")

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
