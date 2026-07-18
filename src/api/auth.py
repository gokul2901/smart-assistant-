from fastapi import APIRouter
from src.models.admin import AdminLogin
from src.services.auth_service import authenticate

router = APIRouter()

@router.post("/admin/login")
def admin_login(data: AdminLogin):

    if authenticate(data.username, data.password):
        return {"message": "Login Success"}

    return {"message": "Invalid Credentials"}



#  Admin User
#     │
#     ▼
# POST /admin/login
#     │
#     ▼
# auth.py (API Route)
#     │
#     ▼
# AdminLogin Model
# (username, password validation)
#     │
#     ▼
# authenticate()
# (Check username & password)
#     │
#  ┌───┴────┐
#  │        │
#  ▼        ▼
# Valid    Invalid
#  │          │
#  ▼          ▼
# Login      Invalid
# Success    Credentials