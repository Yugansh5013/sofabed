from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Shopify ZIP Pricing Engine")

# CRITICAL: Allow your Shopify store to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, swap "*" with your actual store URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what data we expect from the Shopify Front-end
class PriceCheckRequest(BaseModel):
    zip_code: str
    variant_id: Optional[str] = None
    base_price: Optional[float] = None

# Hardcoded assignment lookup rules
ZIP_PRICE_MAP = {
    "75028": 1499.00,
    "10001": 1699.00,
    "90210": 1799.00
}

@app.post("/api/check-price")
async def check_price(payload: PriceCheckRequest):
    # Clean up the input string (remove whitespace/hyphens)
    zip_clean = payload.zip_code.strip()
    
    # Check if the zip code exists in our hardcoded engine
    if zip_clean in ZIP_PRICE_MAP:
        adjusted_price = ZIP_PRICE_MAP[zip_clean]
        return {
            "status": "success",
            "zip_found": True,
            "display_price": f"${adjusted_price:,.2f}",
            "numeric_price": adjusted_price,
            "message": f"Special location rate applied for ZIP {zip_clean}"
        }
    
    # Fallback if ZIP code doesn't match our criteria
    fallback_price = payload.base_price if payload.base_price else 1200.00
    return {
        "status": "success",
        "zip_found": False,
        "display_price": f"${fallback_price:,.2f}",
        "numeric_price": fallback_price,
        "message": "Standard regional pricing applied."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)