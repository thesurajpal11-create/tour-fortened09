import base64
import hashlib
import hmac
import json
import os
from urllib import error, request

from fastapi import HTTPException


RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")


def _require_razorpay_config() -> None:
    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise HTTPException(status_code=500, detail="Razorpay credentials are not configured")


def create_razorpay_order(amount_rupees: float, receipt: str, currency: str = "INR") -> dict:
    _require_razorpay_config()
    payload = json.dumps(
        {
            "amount": int(round(amount_rupees * 100)),
            "currency": currency,
            "receipt": receipt,
            "payment_capture": 1,
        }
    ).encode("utf-8")
    auth = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode("utf-8")).decode("ascii")
    req = request.Request(
        "https://api.razorpay.com/v1/orders",
        data=payload,
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8")
        raise HTTPException(status_code=502, detail=f"Razorpay order failed: {detail}") from exc
    except error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"Razorpay is unreachable: {exc.reason}") from exc


def verify_razorpay_signature(order_id: str, payment_id: str, signature: str) -> bool:
    _require_razorpay_config()
    body = f"{order_id}|{payment_id}".encode("utf-8")
    digest = hmac.new(RAZORPAY_KEY_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)
