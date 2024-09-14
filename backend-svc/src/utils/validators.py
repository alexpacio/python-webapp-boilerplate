REQUIRED_FIELDS = ["name", "email"]
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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