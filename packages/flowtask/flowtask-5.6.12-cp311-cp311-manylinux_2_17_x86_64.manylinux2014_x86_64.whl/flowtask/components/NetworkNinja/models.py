from typing import List, Optional, Union, Any
from datetime import datetime
from datamodel import BaseModel, Field

class Organization(BaseModel):
    orgid: int = Field(required=False)
    org_name: str
    status: bool = Field(required=True, default=True)

    class Meta:
        name: str = 'organizations'
        strict: bool = True

def create_organization(
    name: str,
    value: Any,
    target_type: Any,
    parent_data: BaseModel
) -> Organization:
    org_name = parent_data.get('org_name', None) if parent_data else None
    args = {
        name: value,
        "org_name": org_name,
        "status": True,
    }
    return target_type(**args)

# BaseModel.register_converter(Organization, create_organization, 'orgid')

class Client(BaseModel):
    client_id: int = Field(required=False)
    client_name: str
    status: bool = Field(required=True, default=True)
    orgid: Organization = Field(required=False)
    org_name: str

    class Meta:
        name: str = 'clients'
        strict: bool = True
        as_objects: bool = True

class CustomField(BaseModel):
    custom_id: int = Field(primary_key=True, required=True)
    custom_name: str
    custom_value: Union[str, None]
    custom_client_id: str

class Store(BaseModel):
    org_name: str = Field(required=True)
    store_id: int = Field(primary_key=True, required=True)
    store_name: str = Field(required=True)
    store_address: str
    city: str
    zipcode: str
    phone_number: Optional[str]
    email_address: str = Field(alias="emailAddress")
    store_number: Optional[str]
    store_status: str
    latitude: float
    longitude: float
    timezone: str
    account_id: int
    country_id: str
    created_at: datetime
    updated_at: datetime
    store_type: str
    account_name: str
    visit_rule: List[str]
    visit_category: List[str]
    orgid: List[Organization]
    client_id: List[Client]
    client_name: List[str]
    custom_fields: Optional[List[CustomField]]
    market_name: str
    region_name: str
    district_name: str

    class Meta:
        strict = True
        as_objects = True
