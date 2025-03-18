from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Hash a password using a secure method (SHA-256).
    """
    return generate_password_hash(password)

def verify_password(stored_hash, provided_password):
    """
    Verify a password against a stored hash.
    Returns True if the password matches the hash.
    """
    return check_password_hash(stored_hash, provided_password)
 
