import os
from dotenv import load_dotenv

load_dotenv()

def authenticate(username, password):

    admin_user = os.getenv("ADMIN_USERNAME")
    admin_pass = os.getenv("ADMIN_PASSWORD")

    if username == admin_user and password == admin_pass:
        return True

    return False