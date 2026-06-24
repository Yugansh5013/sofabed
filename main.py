import hmac
import hashlib
import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Production-Grade Secure Shopify Pricing Engine")

# Replace this with your actual Client Secret key from the Shopify Partner Dashboard App settings
SHOPIFY_APP_SECRET = os.getenv("SHOPIFY_APP_SECRET")

class PriceCheckRequest(BaseModel):
    zip_code: str
    variant_id: Optional[str] = None

ZIP_PRICE_MAP = {
    "75028": 1499.00,
    "10001": 1699.00,
    "90210": 1799.00
}

def verify_shopify_proxy_signature(query_params: dict, secret: str) -> bool:
    """
    Computes and verifies the HMAC SHA-256 signature sent by Shopify.
    """
    provided_signature = query_params.get("signature")
    if not provided_signature:
        return False

    # 1. Strip out the signature parameter itself to leave structural validation data
    sorted_params = sorted([f"{k}={v}" for k, v in query_params.items() if k != "signature"])
    message = "".join(sorted_params)

    # 2. Re-hash the message string locally using our private client app secret
    calculated_signature = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    # 3. Securely compare signatures to prevent timing side-channel attacks
    return hmac.compare_digest(provided_signature, calculated_signature)

@app.post("/apps/regional-pricing/api/check-price")
async def check_price(request: Request, payload: PriceCheckRequest):
    # Enforce strict signature checking using the URL query parameters sent by Shopify's proxy engine
    query_params = dict(request.query_params)
    
    if not verify_shopify_proxy_signature(query_params, SHOPIFY_APP_SECRET):
        raise HTTPException(status_code=401, detail="Unauthorized request source: Cryptographic Signature Mismatch")

    zip_clean = payload.zip_code.strip()
    if zip_clean in ZIP_PRICE_MAP:
        adjusted_price = ZIP_PRICE_MAP[zip_clean]
        return {
            "status": "success",
            "zip_found": True,
            "display_price": f"${adjusted_price:,.2f}"
        }
    
    return {
        "status": "success",
        "zip_found": False,
        "display_price": "$1,200.00"
    }