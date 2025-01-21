import hmac
import hashlib
import base64
from datetime import datetime

def generate_signature(secret_key, data):
    """Generate HMAC signature."""
    signature = hmac.new(
        secret_key.encode(), 
        data.encode(), 
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()

def get_timestamp():
    """Get the current timestamp in ISO format."""
    return datetime.utcnow().isoformat()
