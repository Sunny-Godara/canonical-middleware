import xml.etree.ElementTree as ET
from app.models.entities import Application
from datetime import datetime

def xml_to_application(xml_data: str) -> Application:
    # 1. Parse the actual XML (root is <TaxpayerProfile>)
    root = ET.fromstring(xml_data)
    
    # 2. Extract the specific fields from your Revenue mock data
    pan = root.findtext("PAN", default="UNKNOWN")
    
    name_node = root.find("Name")
    first_name = name_node.findtext("First", default="") if name_node is not None else ""
    last_name = name_node.findtext("Last", default="") if name_node is not None else ""
    full_name = f"{first_name} {last_name}".strip()
    
    # Calculate age based on the <DOB> format (DD/MM/YYYY)
    dob_string = root.findtext("DOB", default="01/01/1990")
    birth_year = int(dob_string.split("/")[-1])
    current_year = 2026
    calculated_age = current_year - birth_year
    
    status_text = root.findtext("Status", default="PENDING")
    
    # 3. Construct the Canonical Application Model
    application = Application(
        application_id=f"REV-{pan}",
        citizen={
            "citizen_id": pan,
            "name": full_name,
            "age": calculated_age,
            "email": "not_provided@revenue.mock.in" # Not in XML, using default
        },
        department="Revenue",
        application_type="Tax Verification",
        status=status_text,
        schema_version="1.0"
    )
    
    return application
