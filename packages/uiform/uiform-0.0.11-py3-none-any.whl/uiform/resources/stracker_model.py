from pydantic import BaseModel, BeforeValidator, Field, EmailStr, field_serializer
from typing import Annotated
from typing import Optional, Literal
import datetime
from cubeblock.dataclasses.validators import notnan, validate_country_code, validate_date, validate_time, validate_bool, validate_str, validate_phone_number, validate_email_address, validate_float, validate_integer

TimeField = Annotated[datetime.time, Field(json_schema_extra={"format": "iso-time"})]


class PickupDeliveryDatetimeData(BaseModel):
    date: Annotated[Optional[datetime.date], BeforeValidator(validate_date)] = Field(default=None, description="Date of the pickup/delivery. ISO 8601 Date Format: YYYY-MM-DD")
    start_time: Annotated[Optional[TimeField], BeforeValidator(validate_time)] = Field(default=None, description="Start time of the pickup/delivery. ISO 8601 Time Format: hh:mm")
    end_time: Annotated[Optional[TimeField], BeforeValidator(validate_time)] = Field(default=None, description="End time of the pickup/delivery. ISO 8601 Time Format: hh:mm. Must be greater than or equal to the start_time.")


    @field_serializer('date', 'start_time', 'end_time')
    def serialize_date_or_time(self, date_or_time_value: Optional[datetime.date | datetime.time]) -> Optional[str]:
        if date_or_time_value is None:
            return None
        return date_or_time_value.isoformat()



class AddressData(BaseModel):
    line1: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Address line 1 (e.g., street, PO Box, or company name).")
    line2: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Address line 2 (e.g., apartment, suite, unit, or building).")
    city: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="City, district, suburb, town, or village.")
    state: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="State, county, province, or region.")
    postal_code: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="ZIP or postal code. If french postal code, it should be a pure number, without letters.")
    country: Annotated[Optional[str], BeforeValidator(validate_country_code)] = Field(default=None, description="Two-letter country code (ISO 3166-1 alpha-2).")

    @property
    def line(self) -> str:
        nonNan_values = [x for x in [self.line1, self.line2] if notnan(x)]
        return ' '.join(nonNan_values)  # type: ignore

    @property
    def flat_address(self) -> str:
        nonNan_values = [x for x in [self.line1, self.line2, self.city, self.state, self.postal_code, self.country] if notnan(x)]
        return ' '.join(nonNan_values)  # type: ignore


class SenderData(BaseModel):
    company_name: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Name of the company.")
    observations: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Observations about the sender.")
    address: AddressData = Field(default=AddressData(), description="Address of the sender.")
    phone_number: Annotated[Optional[str], BeforeValidator(validate_phone_number)] = Field(default=None, description="Phone number of the sender.")
    email_address: Annotated[Optional[EmailStr], BeforeValidator(validate_email_address)] = Field(default=None, description="Email address of the sender.")
    pickup_datetime: PickupDeliveryDatetimeData = Field(default=PickupDeliveryDatetimeData(), description="pickup date and time in ISO 8601 format")

    def __str__(self) -> str:
        return str(self.company_name) + " " + self.address.flat_address

class RecipientData(BaseModel):
    company_name: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Name of the company.")
    observations: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Observations about the recipient.")
    address: AddressData = Field(default=AddressData(), description="Address of the recipient.")
    phone_number: Annotated[Optional[str], BeforeValidator(validate_phone_number)] = Field(default=None, description="Phone number of the recipient.")
    email_address: Annotated[Optional[EmailStr], BeforeValidator(validate_email_address)] = Field(default=None, description="Email address of the recipient.")
    delivery_datetime: PickupDeliveryDatetimeData = Field(default=PickupDeliveryDatetimeData(), description="delivery date and time")

    def __str__(self) -> str:
        return str(self.company_name) + " " + self.address.flat_address

from typing import Any

from enum import StrEnum
class Incoterm(StrEnum):
    EXW = "EXW"
    FCA = "FCA"
    FAS = "FAS"
    FOB = "FOB"
    CPT = "CPT"
    CFR = "CFR"
    CIF = "CIF"
    CIP = "CIP"
    DPU = "DPU"
    DAP = "DAP"
    DDP = "DDP"
    DAF = "DAF"
    DAT = "DAT"
    DES = "DES"
    DEQ = "DEQ"
    DDU = "DDU"

def validate_incoterm(v: Any) -> Optional[Incoterm]:
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip().upper()
        if v in ('', 'NULL', 'NONE', 'NAN'):
            return None
        if v in Incoterm.__members__:
            return Incoterm(v)
    return None
    


class AirFreightClient(BaseModel):
    account: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Client account identifier")
    client_reference: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Client's reference for this shipment")
    ordering_party: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Name of the party ordering the shipment")
    transport_type: Annotated[Optional[Literal['Air', 'Road']], BeforeValidator(validate_str)] = Field(default=None, description="Type of transport: Air or Road")
    incoterm: Annotated[Optional[Incoterm], BeforeValidator(validate_incoterm)] = Field(default=None, description="International Commercial Terms for the shipment")

class AirPackage(BaseModel):
    quantity: Annotated[Optional[int], BeforeValidator(validate_integer)] = Field(default=None, description="Number of packages in the shipment")
    weight: Annotated[Optional[float], BeforeValidator(validate_float)] = Field(default=None, description="Weight of the package in kg")
    length: Annotated[Optional[float], BeforeValidator(validate_float)] = Field(default=None, description="Length of the package in cm")
    width: Annotated[Optional[float], BeforeValidator(validate_float)] = Field(default=None, description="Width of the package in cm")
    height: Annotated[Optional[float], BeforeValidator(validate_float)] = Field(default=None, description="Height of the package in cm")
    description: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Brief description of the package contents")
    content: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Detailed description of the package contents")

class AirServices(BaseModel):
    return_trip: Annotated[Optional[bool], BeforeValidator(validate_bool)] = Field(default=False, description="Indicates if a return trip is required")
    loading_tailgate: Annotated[Optional[bool], BeforeValidator(validate_bool)] = Field(default=False, description="Indicates if a loading tailgate is needed")
    economical: Annotated[Optional[bool], BeforeValidator(validate_bool)] = Field(default=False, description="Indicates if economical shipping is requested")
    urgent: Annotated[Optional[bool], BeforeValidator(validate_bool)] = Field(default=False, description="Indicates if urgent shipping is requested")
    dangerous_goods: Annotated[Optional[bool], BeforeValidator(validate_bool)] = Field(default=False, description="Indicates if the shipment contains dangerous goods")
    departure_airport: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Departure airport")
    arrival_airport: Annotated[Optional[str], BeforeValidator(validate_str)] = Field(default=None, description="Arrival airport")

class AirBookingConfirmationData(BaseModel):
    client: AirFreightClient = Field(default=AirFreightClient(), description="Client data")
    package: AirPackage = Field(default=AirPackage(), description="Package data")
    services: AirServices = Field(default=AirServices(), description="Air services data")
    sender: SenderData = Field(default=SenderData(), description="Sender data")
    recipient: RecipientData = Field(default=RecipientData(), description="Recipient data")