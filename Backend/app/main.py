from fastapi import FastAPI
from app.core import config as _config
from app.core.router import register_routers

app = FastAPI(
    title="My API", version="1.0", docs_url="/docs" if _config.ENV == "dev" else None
)

register_routers(app)

@app.get("/health")
def health() -> dict[str, str]:
    """Return a basic health status."""
    return {"status": "ok"}
