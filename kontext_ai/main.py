"""FastAPI app with Nuxt.js frontend"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from kontext_ai.api import llm, settings
from kontext_ai.utils import HOST, IS_LOCAL, CLIENT_APP_DIR, PORT

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    f"http://localhost:{PORT}",
    f"http://127.0.0.1::{PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type"],
)

# Serve Nuxt app static files in development
if IS_LOCAL:
    app.mount(
        "/client", StaticFiles(directory=CLIENT_APP_DIR, html=True), name="client-app"
    )


@app.get("/api/hello")
async def hello():
    """Example FastAPI endpoint"""
    return {"message": f"Hello from {os.getenv('KONTEXT_AI_APP_NAME')}!"}


# Include the router in the FastAPI app
app.include_router(llm.router)
app.include_router(settings.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )
