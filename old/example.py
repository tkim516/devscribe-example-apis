from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI(title="Custom Swagger API", version="1.0.0")

# Mount static files (for serving custom CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load templates (for serving custom Swagger UI)
templates = Jinja2Templates(directory="templates")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(request: Request):
    """Serve the custom Swagger UI."""
    return templates.TemplateResponse("swagger.html", {"request": request})

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
