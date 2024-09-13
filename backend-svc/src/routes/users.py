from typing import Annotated
from fastapi import APIRouter, status, Request, Form, File, UploadFile
from pydantic import BaseModel
from werkzeug.utils import secure_filename
from services.users import create_user, get_all_users, uploader
import json


REQUIRED_FIELDS = ["name", "email"]
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

router = APIRouter()


def validate_user_data(data):
    """
    Validates the user data.

    This function checks if the provided user data contains all the required fields.
    It returns an error message and HTTP status code if any required field is missing.

    Args:
        data (dict): The user data to be validated.

    Returns:
        Tuple[str, int]: Error message and HTTP status code if validation fails, otherwise (None, None).
    """

    if not data:
        return "Missing required data", 400
    for field in REQUIRED_FIELDS:
        if field not in data:
            return f"Missing required data: {field}", 400
    return None, None


def allowed_file(filename):
    """
    Check if the file is allowed.
    
    Args:
        filename (str): The filename to check.

    Returns:
        bool: True if allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

@router.post("/users/", tags=["users"])
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
        return json.dumps({"error": error_message}), status_code

    if avatar and allowed_file(avatar.filename):
        filename = secure_filename(avatar.filename)
        avatar_url = uploader(avatar.file, filename)
        if not avatar_url:
            return json.dumps({"error": "Avatar upload failed"}), 500
        user_data['avatar_url'] = avatar_url
    else:
        return json.dumps({"error": "Invalid file type or no file uploaded"}), 400

    print(user_data)
    return create_user(user_data)