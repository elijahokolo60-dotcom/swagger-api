from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="My API",
    description="API for managing users and products",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc",  # Alternative ReDoc at /redoc
    openapi_url="/openapi.json"  # OpenAPI JSON at /openapi.json
)

# Define Pydantic models
class UserBase(BaseModel):
    email: str = Field(..., example="john@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="secret123")

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: Optional[str] = None

# Health check endpoint
@app.get("/", tags=["Health"])
def root():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

# Users endpoints
@app.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_users(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return")
):
    """
    Retrieve all users with pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    mock_users = [
        UserResponse(
            id=1,
            email="john@example.com",
            full_name="John Doe",
            is_active=True,
            created_at=datetime.now()
        )
    ]
    return mock_users

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(
    user_id: int = Path(..., description="The ID of the user to retrieve", gt=0)
):
    """
    Get a specific user by ID.
    
    - **user_id**: The ID of the user (must be greater than 0)
    """
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user_id,
        email="john@example.com",
        full_name="John Doe",
        is_active=True,
        created_at=datetime.now()
    )

@app.post("/users", response_model=UserResponse, tags=["Users"], status_code=201)
def create_user(user: UserCreate):
    """
    Create a new user.
    
    - **user**: User data including email and password
    """
    return UserResponse(
        id=2,
        email=user.email,
        full_name=user.full_name,
        is_active=True,
        created_at=datetime.now()
    )

@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(
    user_id: int,
    user: UserBase = Body(..., description="Updated user data")
):
    """
    Update an existing user.
    
    - **user_id**: The ID of the user to update
    - **user**: Updated user data
    """
    return UserResponse(
        id=user_id,
        email=user.email,
        full_name=user.full_name,
        is_active=True,
        created_at=datetime.now()
    )

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int):
    """
    Delete a user by ID.
    
    - **user_id**: The ID of the user to delete
    """
    return {"message": f"User {user_id} deleted successfully"}

# Products endpoints
@app.get("/products", response_model=List[Product], tags=["Products"])
def get_products(category: Optional[str] = Query(None, description="Filter by category")):
    """
    Get all products, optionally filtered by category.
    """
    products = [
        Product(id=1, name="Laptop", price=999.99, category="Electronics"),
        Product(id=2, name="Book", price=19.99, category="Books"),
    ]
    
    if category:
        products = [p for p in products if p.category == category]
    
    return products

# FIXED: Custom OpenAPI configuration without recursion
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    # Use get_openapi instead of app.openapi() to avoid recursion
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add server information
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server"
        }
    ]
    
    # Add tags metadata
    openapi_schema["tags"] = [
        {
            "name": "Users",
            "description": "Operations with users"
        },
        {
            "name": "Products",
            "description": "Operations with products"
        },
        {
            "name": "Health",
            "description": "Health check endpoints"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Assign the custom function
app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)