import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents
from schemas import Product, Inquiry

app = FastAPI(title="SK Furniture Home Decoration API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "name": "SK Furniture Home Decoration",
        "message": "Welcome to SK Furniture API",
    }

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ------------------ Catalog Endpoints ------------------

@app.get("/api/products", response_model=List[Product])
def list_products(category: Optional[str] = None, featured: Optional[bool] = None, limit: int = 50):
    """List products with optional filters"""
    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if featured is not None:
        filter_dict["featured"] = featured
    docs = get_documents("product", filter_dict, limit)
    # Convert ObjectId to string and coerce fields
    for d in docs:
        d["id"] = str(d.get("_id"))
        d.pop("_id", None)
    return docs

@app.post("/api/products", status_code=201)
def create_product(product: Product):
    """Create a new product"""
    inserted_id = create_document("product", product)
    return {"id": inserted_id}

# ------------------ Inquiry Endpoints ------------------

@app.post("/api/inquiry", status_code=201)
def submit_inquiry(inquiry: Inquiry):
    """Store customer inquiry/lead"""
    inserted_id = create_document("inquiry", inquiry)
    return {"id": inserted_id, "message": "Inquiry received"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
