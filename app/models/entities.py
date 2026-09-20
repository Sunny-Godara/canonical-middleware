from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Citizen(BaseModel):
    citizen_id: str
    name: str
    age: int = Field(ge=0)
    email: Optional[EmailStr] = None


class Application(BaseModel):
    application_id: str
    citizen: Citizen
    department: str
    application_type: str
    status: str
    schema_version: str = "1.0"