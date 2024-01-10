import importlib
import os
import re
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from .database import SessionLocal

# models.Base.metadata.create_all(bind=engine) # create tables

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

resource = {}


# use lifespan to fulfill things required during initiation
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("init lifespan")

    resource["greeting"] = "Capybaramen wish you a good day!"

    # loads api routes
    modules = []
    for file_name in os.listdir(BASE_DIR):
        if (
                file_name.startswith("api")
                and os.path.isdir(os.path.join(BASE_DIR, file_name))
                and os.path.exists(os.path.join(BASE_DIR, file_name, "views.py"))
        ):
            print(f"Configuring {file_name} into app router")
            match_obj = re.match(r"(api)_(\w+)", file_name)

            if match_obj:
                service_type = match_obj.group(1)
                service_name = match_obj.group(2)
                modules.append((service_type, service_name, file_name))
            print("modules: %s", modules)

        for service_type, service_name, file_name in modules:
            module = importlib.import_module("{}.views".format(file_name))
            if getattr(module, "router", None):
                app.include_router(
                    module.router,
                    prefix="/{}/{}".format(service_type, service_name),
                    tags=[service_name]
                )

    # TODO: cache
    # TODO: dramatiq
    yield

    resource.clear()
    print("clean up lifespan")
    print(resource)


app = FastAPI(lifespan=app_lifespan)

# app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
origins = [
    "http://localhost",
    "http://localhost:3333",
    "http://3.143.58.231",
    "http://3.143.58.231:3333"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hi")
def root():
    result = resource["greeting"]
    return {
        "message": result
    }


# Dependency
def get_db():
    print("init db")
    db = SessionLocal()
    try:
        yield db
    finally:
        print("close db")
        db.close()


@app.get("/health_check")
def get_todos(db: Session = Depends(get_db)):
    return "HELLO WORLD"


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Capybaramen TODO app",
        version="0.1.0",
        description="Just an ordinary todo app",
        routes=app.routes
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
