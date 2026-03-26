import logging
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.address import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
    NearbyAddressResponse,
)
from app.services.address_service import AddressService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
)
def create_address(
    payload: AddressCreate,
    db: Session = Depends(get_db),
) -> AddressResponse:
    logger.info("POST /addresses called")
    address = AddressService.create_address(db=db, payload=payload)
    return address


@router.get(
    "/nearby",
    response_model=list[NearbyAddressResponse],
    summary="Find nearby addresses within a given distance",
)
def get_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90, description="Reference latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Reference longitude"),
    distance_km: float = Query(..., gt=0, description="Maximum distance in kilometers"),
    db: Session = Depends(get_db),
) -> Sequence[NearbyAddressResponse]:
    logger.info(
        "GET /addresses/nearby called with lat=%s lon=%s distance=%s",
        latitude,
        longitude,
        distance_km,
    )

    return AddressService.get_nearby_addresses(
        db=db,
        latitude=latitude,
        longitude=longitude,
        max_distance_km=distance_km,
    )


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Get address by ID",
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
) -> AddressResponse:
    logger.info("GET /addresses/%s called", address_id)

    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found.",
        )

    return address


@router.patch(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Update an existing address",
)
def update_address(
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
) -> AddressResponse:
    logger.info("PATCH /addresses/%s called", address_id)

    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found.",
        )

    updated_address = AddressService.update_address(
        db=db,
        address=address,
        payload=payload,
    )
    return updated_address


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an address",
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
) -> Response:
    logger.info("DELETE /addresses/%s called", address_id)

    address = AddressService.get_address_by_id(db=db, address_id=address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found.",
        )

    AddressService.delete_address(db=db, address=address)
    return Response(status_code=status.HTTP_204_NO_CONTENT)