from fastapi import FastAPI

app = FastAPI(title="FastAPI Test API", version="1.0.0")

@app.get("/users")
async def get_users():
    """Retrieve a list of users."""
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@app.post("/users")
async def create_user(name: str):
    """Create a new user with the given name."""
    return {"id": 3, "name": name}