# Shopify ZIP Pricing Engine

A simple FastAPI-based regional pricing lookup service designed to integrate with a Shopify front-end. It allows looking up product pricing based on the customer's ZIP/postal code.

## Features
- **FastAPI Backend**: Fast, modern, and auto-documented API.
- **CORS Support**: Configured to allow requests from cross-origin clients (e.g., Shopify storefronts).
- **ZIP-based Price Lookup**: Returns custom pricing if a ZIP code matches specific hardcoded records, otherwise falls back to a standard price.

## Requirements
- Python 3.8+

## Setup & Installation

1. **Clone the repository** (if not already done).
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```
3. **Activate the virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI application with:
```bash
python main.py
```
The server will start at `http://localhost:8000`. You can access the interactive Swagger API documentation at `http://localhost:8000/docs`.

## API Endpoints

### Check Price
- **Endpoint**: `POST /api/check-price`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "zip_code": "75028",
    "variant_id": "optional_variant_id",
    "base_price": 1200.00
  }
  ```
- **Response (Match Found)**:
  ```json
  {
    "status": "success",
    "zip_found": true,
    "display_price": "$1,499.00",
    "numeric_price": 1499.00,
    "message": "Special location rate applied for ZIP 75028"
  }
  ```
- **Response (No Match / Fallback)**:
  ```json
  {
    "status": "success",
    "zip_found": false,
    "display_price": "$1,200.00",
    "numeric_price": 1200.00,
    "message": "Standard regional pricing applied."
  }
  ```
