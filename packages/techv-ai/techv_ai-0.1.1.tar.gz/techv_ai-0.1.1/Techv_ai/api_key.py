import uuid

def generate_api_key(user_id):
    return f"{user_id}-{uuid.uuid4()}"

def validate_api_key(api_key):
    # Basic example of validation logic
    return len(api_key.split("-")) == 2
