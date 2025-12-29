MODULE: main_fixed.py

IMPORTS:
  fastapi
  pydantic
  typing
  datetime

DEFINE MODELS:
  UserBase: email, full_name(optional)
  UserCreate: inherits UserBase, adds password
  UserResponse: inherits UserBase, adds id, is_active, created_at

CREATE FastAPI APP:
  app = FastAPI(title="My API", description="API Documentation", version="1.0.0")

DEFINE ENDPOINTS:
  GET /users:
    FUNCTION get_users():
      PARAMETERS: skip, limit
      RETURNS: List[UserResponse]
      DOCSTRING: Retrieve all users with pagination

  GET /users/{user_id}:
    FUNCTION get_user(user_id):
      PARAMETERS: user_id (path parameter)
      RETURNS: UserResponse
      DOCSTRING: Get a specific user by ID

DEFINE custom_openapi FUNCTION:
  IF app.openapi_schema exists:
    RETURN app.openapi_schema
  
  CALL get_openapi() to generate schema
  ADD security schemes to schema
  ADD servers information to schema
  ADD tags metadata to schema
  
  SET app.openapi_schema = modified schema
  RETURN app.openapi_schema

ASSIGN custom function:
  app.openapi = custom_openapi

RUN SERVER:
  START uvicorn server on port 8000
