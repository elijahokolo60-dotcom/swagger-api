from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Create FastAPI app with metadata
app = FastAPI(
    title="My API",
    description="API for managing users and products",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc",  # Alternative ReDoc at /redoc
    openapi_url="/openapi.json",  # OpenAPI JSON at /openapi.json
    
    # Additional OpenAPI metadata
    openapi_tags=[
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
    ],
    
    # Servers information
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server"
        }
    ]
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)