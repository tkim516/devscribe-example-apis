from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI(title="FastAPI Test API", version="1.0.0")

# Enable CORS for all origins and all methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin; adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods; limit as necessary
    allow_headers=["*"],  # Allows all headers; limit as necessary
)

user_list: List[Dict[str, int]] = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.get("/users")
async def get_users():
    """Retrieve a list of users."""
    return user_list

@app.post("/users")
async def create_user(request: Request):
    """Create a new user with the given name."""
    data = await request.json()  # Read and parse JSON from the request
    name = data.get("name")      # Extract the name from JSON payload
    if name is None:
        return {"error": "Name is required"}
    user_id = len(user_list) + 1
    new_user = {"id": user_id, "name": name}
    user_list.append(new_user)
    return user_list