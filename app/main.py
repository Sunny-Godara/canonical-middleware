from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
import logging

# Dev 3: Your fetcher service
from app.services.fetcher import DepartmentDataFetcher

# Dev 1 & 2: Shreya's adapter and models
from app.models.entities import Application
from app.adapters.xml_adapter import xml_to_application
from app.services.validator import validate_canonical_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Canonical Middleware",
    description="Federated schema translation and routing gateway",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error at {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal System Error", "detail": str(exc)}
    )

@app.get("/health", tags=["Platform"])
def root():
    return {"status": "Canonical Middleware API is running"}

@app.get("/api/v1/federate-citizen", tags=["Integration"])
async def process_citizen_application():
    """Fetches raw XML and translates it to Canonical Model."""
    try:
        # 1. Fetch raw data
        xml_data, json_data = await DepartmentDataFetcher.fetch_department_data()

        # 2. Translate XML to canonical model
        canonical_application = xml_to_application(xml_data)

        # 3. Validate against strict rules
        validate_canonical_data(canonical_application.model_dump())

        # 4. Return clean JSON
        return {
            "status": "success",
            "message": "Data fetched and translated successfully",
            "data": canonical_application
        }

    except RuntimeError as err:
        raise HTTPException(status_code=502, detail=str(err))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Data translation failed: {str(e)}")
