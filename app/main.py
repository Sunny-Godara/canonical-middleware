from fastapi import FastAPI, HTTPException
from app.models.entities import Application
from app.adapters.xml_adapter import xml_to_application
from app.services.validator import validate_canonical_data


app = FastAPI(
    title="Canonical Middleware",
    description="Middleware for canonical application data",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Canonical Middleware API is running"}


@app.post("/applications")
def create_application(application: Application):
    try:
        validate_canonical_data(application.model_dump())
        return {
            "message": "Application accepted",
            "data": application
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/convert/xml")
def convert_xml(xml_data: str):
    try:
        application = xml_to_application(xml_data)
        return {
            "message": "XML converted successfully",
            "data": application
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))