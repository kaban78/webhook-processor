from datetime import datetime
from typing import Any

def webhook_document(event_type: str, raw_body: bytes, payload: dict[str, Any]) -> dict:
    return {
        "event_type": event_type,
        "received_at": datetime.utcnow(),
        "raw_body": raw_body,
        "payload": payload,
    }
