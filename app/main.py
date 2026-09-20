from fastapi import FastAPI, HTTPException, status
from app.services.fetcher import DepartmentDataFetcher

app = FastAPI(
    title="Interoperability Gateway",
    description="Federated schema translation and routing gateway",
    version="1.0.0"
)

@app.get("/health", tags=["Platform"])
def health_check():
    return {"status": "online", "role": "Traffic Controller"}

@app.get("/api/v1/fetch-raw-records", tags=["Orchestration"])
async def get_raw_department_records():
    """
    Triggers Developer 3's httpx client to pull upstream legacy 
    records from both department mock servers.
    """
    try:
        xml_data, json_data = await DepartmentDataFetcher.fetch_department_data()
        return {
            "status": "success",
            "revenue_raw_xml": xml_data,
            "transport_raw_json": json_data
        }
    except RuntimeError as err:
        # Translate internal service failure into an explicit HTTP 502 Bad Gateway
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(err)
        )
