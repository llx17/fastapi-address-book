from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddressBase(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Optional label for the address, e.g. Home or Office",
    )
    latitude: float = Field(
        ...,
        description="Latitude of the address",
        examples=[10.8505],
    )
    longitude: float = Field(
        ...,
        description="Longitude of the address",
        examples=[76.2711],
    )

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return value


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Optional label for the address, e.g. Home or Office",
    )
    latitude: float | None = Field(
        default=None,
        description="Latitude of the address",
        examples=[10.8505],
    )
    longitude: float | None = Field(
        default=None,
        description="Longitude of the address",
        examples=[76.2711],
    )

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float | None) -> float | None:
        if value is not None and not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float | None) -> float | None:
        if value is not None and not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return value


class AddressResponse(BaseModel):
    id: int
    name: str | None
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)