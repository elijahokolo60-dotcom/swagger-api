MODULE: main_simple.py

IMPORTS:
  fastapi
  pydantic
  typing
  datetime

DEFINE MODELS:
  UserBase: email, full_name(optional)
  UserCreate: inherits UserBase, adds password
  UserResponse: inherits UserBase, adds id, is_active, created_at

CREATE FastAPI APP WITH METADATA:
  app = FastAPI(
    title = "My API",
    description = "API Documentation",
    version = "1.0.0",
    docs_url = "/docs",
    redoc_url = "/redoc",
    openapi_url = "/openapi.json",
    openapi_tags = [
      {"name": "Users", "description": "Operations with users"},
      {"name": "Health", "description": "Health checks"}
    ],
    servers = [
      {"url": "http://localhost:8000", "description": "Dev server"},
      {"url": "https://api.example.com", "description": "Prod server"}
    ]
  )

DEFINE ENDPOINTS:
  GET / (tagged "Health"):
    FUNCTION root():
      RETURNS: JSON with status and timestamp
      DOCSTRING: Health check endpoint

  GET /users (tagged "Users"):
    FUNCTION get_users(skip, limit):
      PARAMETERS: skip (default 0), limit (default 10)
      RETURNS: List[UserResponse]
      DOCSTRING: Retrieve all users with pagination

  GET /users/{user_id} (tagged "Users"):
    FUNCTION get_user(user_id):
      PARAMETERS: user_id (must be > 0)
      RETURNS: UserResponse
      DOCSTRING: Get a specific user by ID

RUN SERVER:
  START uvicorn server on port 8000
