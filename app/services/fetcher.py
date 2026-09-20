import httpx
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

# Inside Docker, use container network names; fallback to localhost for local testing
REVENUE_URL = "http://mock-revenue:8001/revenue_response.xml"
TRANSPORT_URL = "http://mock-transport:8002/transport_response.json"

class DepartmentDataFetcher:
    @staticmethod
    async def fetch_department_data() -> Tuple[str, str]:
        """
        Asynchronously fetches legacy records from Revenue and Transport services.
        Returns:
            Tuple[str, str]: (raw_xml_string, raw_json_string)
        """
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                # 1. Query Revenue Mock
                rev_resp = await client.get(REVENUE_URL)
                rev_resp.raise_for_status()
                revenue_xml = rev_resp.text

                # 2. Query Transport Mock
                trans_resp = await client.get(TRANSPORT_URL)
                trans_resp.raise_for_status()
                transport_json = trans_resp.text

                return revenue_xml, transport_json

            except httpx.RequestError as exc:
                logger.error(f"Network failure while reaching upstream department: {exc}")
                raise RuntimeError(f"Upstream service unreachable: {exc.request.url}")
            except httpx.HTTPStatusError as exc:
                logger.error(f"Upstream department returned error status: {exc.response.status_code}")
                raise RuntimeError(f"Department service returned error: {exc.response.status_code}")
