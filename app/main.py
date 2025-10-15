from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .users import models as user_models
from .projects import models as project_models
from .documents import models as document_models
from .finance import models as finance_models

user_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BuildBuzz API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:3001",  # Alternative React port
        "http://localhost:8080",  # Vue.js default
        "http://localhost:4200",  # Angular default
        "http://localhost:5173",  # Vite default
        "http://localhost:5174",  # Alternative Vite port
        "http://127.0.0.1:3000",  # Alternative localhost format
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
        # Add your production frontend URL here when deploying
        # "https://your-frontend-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the BuildBuzz API"}

from .users.api import router as users_router
from .projects.api import router as projects_router
from .documents.api import router as documents_router
from .finance.api import router as finance_router

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(projects_router, prefix="", tags=["projects"])
app.include_router(documents_router, prefix="/documents", tags=["documents"])
app.include_router(finance_router, prefix="", tags=["finance"])
