import hmac
import hashlib

def verify_signature(secret: str, body: bytes, signature_header: str | None) -> bool:
    if not signature_header:
        return False
    try:
        algo, signature = signature_header.split("=", 1)
        if algo != "sha256":
            return False
    except ValueError:
        return False

    expected = hmac.new(
        secret.encode("utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
