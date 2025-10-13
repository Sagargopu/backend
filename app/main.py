from fastapi import FastAPI

from .database import engine
from .users import models as user_models
from .projects import models as project_models
from .documents import models as document_models
from .finance import models as finance_models
from .payroll import models as payroll_models
from .payroll import models as payroll_models

user_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BuildBuzz API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the BuildBuzz API"}

from .users.api import router as users_router
from .projects.api import router as projects_router
from .documents.api import router as documents_router
from .finance.api import router as finance_router
from .payroll.api import router as payroll_router

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(projects_router, prefix="", tags=["projects"])
app.include_router(documents_router, prefix="", tags=["documents"])
app.include_router(finance_router, prefix="", tags=["finance"])
app.include_router(payroll_router, prefix="", tags=["payroll"])
