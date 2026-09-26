from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Enterprise Capability & Delivery Governance Platform — "
        "IBM Bob Hackathon Submission"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# Register routers
from app.api import teams, squads, employees, skills, projects  # noqa: E402
from app.api import authorizations, metrics, allocations, dashboard, ai, demo  # noqa: E402
from app.api import project_hub  # noqa: E402

app.include_router(teams.router, prefix="/api/v1")
app.include_router(squads.router, prefix="/api/v1")
app.include_router(employees.router, prefix="/api/v1")
app.include_router(skills.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(project_hub.router, prefix="/api/v1")
app.include_router(authorizations.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")
app.include_router(allocations.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(demo.router)
