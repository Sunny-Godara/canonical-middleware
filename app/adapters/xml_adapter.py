import xml.etree.ElementTree as ET

from app.models.entities import Application


def xml_to_application(xml_data: str) -> Application:
    root = ET.fromstring(xml_data)

    citizen = root.find("citizen")

    application = Application(
        application_id=root.findtext("application_id"),
        citizen={
            "citizen_id": citizen.findtext("citizen_id"),
            "name": citizen.findtext("name"),
            "age": int(citizen.findtext("age")),
            "email": citizen.findtext("email")
        },
        department=root.findtext("department"),
        application_type=root.findtext("application_type"),
        status=root.findtext("status"),
        schema_version=root.findtext("schema_version")
    )

    return application