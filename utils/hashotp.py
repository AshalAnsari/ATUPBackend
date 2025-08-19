import hashlib

def hash_otp(otp: str) -> str:
    """
    Hash the OTP using SHA-256 for secure storage in DB.
    """
    return hashlib.sha256(otp.encode()).hexdigest()