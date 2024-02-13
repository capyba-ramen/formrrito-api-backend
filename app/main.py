import importlib
import os
import re
from contextlib import asynccontextmanager
from typing import Union

from fastapi import Depends, FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from api_tool import actions as tool_actions
from api_tool import schemas as tool_schemas
# from . import auth
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
    "https://3.143.58.231",
    "https://3.143.58.231:3333",
    "https://www.formrrito.fun"
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
    # result = resource["greeting"]
    return "Hello World"


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


# note: 由於發現在 api_* 層使用 UploadFile 會導致 swagger 無法正確顯示，因此將 upload_image 移至此層
@app.post(
    "/upload_image",
    description="上傳圖片(用於 form & question)",
    response_model=Union[bool, str]
)
async def upload_image(
        inputs: tool_schemas.UploadImageInForm = Depends(tool_schemas.UploadImageInForm.as_form),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    result = await tool_actions.upload_image(inputs, file, db)
    return result


@app.delete(
    "/image",
    description="刪除圖片 (image_id 為 form & question 中的 image_url)",
    response_model=bool
)
async def delete_image(
        inputs: tool_schemas.DeleteImageIn = Body(..., title="刪除圖片"),
        db: Session = Depends(get_db)
):
    result = await tool_actions.delete_image(inputs, db)
    return result


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Formrrito",
        version="0.1.0",
        description="Just an ordinary form generator",
        routes=app.routes
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
