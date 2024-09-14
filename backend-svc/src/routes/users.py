from typing import Annotated
from fastapi import APIRouter, status, Request, Form, File, UploadFile
from pydantic import BaseModel
from werkzeug.utils import secure_filename
from services.users import create_user, get_all_users, uploader
from utils.validators import allowed_file, validate_user_data
import json


router = APIRouter()


@router.get("/users/", tags=["users"], status_code=status.HTTP_200_OK)
def get_users():
    """
    Endpoint to get all users.

    This endpoint handles GET requests to fetch all users from the DynamoDB table.

    Returns:
        Tuple[Response, int]: JSON response containing the list of users and HTTP status code.
    """

    try:
        return get_all_users()
    except(e):
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/users/", tags=["users"], status_code=status.HTTP_201_CREATED)
def post_user(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    avatar: Annotated[UploadFile, File()],
):
    """
    Endpoint to create a new user.

    This endpoint handles POST requests to create a new user in the DynamoDB table.
    It validates the user data before attempting to create the user.

    Returns:
        Tuple[Response, int]: JSON response indicating success or failure and HTTP status code.
    """

    user_data = {
        'name': name,
        'email': email
    }
    error_message, status_code = validate_user_data(user_data)

    if error_message:
        raise HTTPException(status_code=status_code, detail=error_message)

    if avatar and allowed_file(avatar.filename):
        filename = secure_filename(avatar.filename)
        avatar_url = uploader(avatar.file, filename)
        if not avatar_url:
            raise HTTPException(status_code=500, detail="Avatar upload failed")
        user_data['avatar_url'] = avatar_url
    else:
        raise HTTPException(status_code=400, detail="Invalid file type or no file uploaded")

    return create_user(user_data)