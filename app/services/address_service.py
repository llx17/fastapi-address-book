import logging

from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.utils.distance import calculate_distance_km

logger = logging.getLogger(__name__)


class AddressService:
    @staticmethod
    def create_address(db: Session, payload: AddressCreate) -> Address:
        logger.info("Creating a new address with name=%s", payload.name)

        address = Address(
            name=payload.name,
            latitude=payload.latitude,
            longitude=payload.longitude,
        )

        db.add(address)
        db.commit()
        db.refresh(address)

        logger.info("Address created successfully with id=%s", address.id)
        return address

    @staticmethod
    def get_address_by_id(db: Session, address_id: int) -> Address | None:
        logger.info("Fetching address with id=%s", address_id)

        address = db.query(Address).filter(Address.id == address_id).first()

        if address:
            logger.info("Address found with id=%s", address_id)
        else:
            logger.warning("Address not found with id=%s", address_id)

        return address

    @staticmethod
    def update_address(
        db: Session,
        address: Address,
        payload: AddressUpdate,
    ) -> Address:
        logger.info("Updating address with id=%s", address.id)

        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(address, field, value)

        db.commit()
        db.refresh(address)

        logger.info("Address updated successfully with id=%s", address.id)
        return address

    @staticmethod
    def delete_address(db: Session, address: Address) -> None:
        logger.info("Deleting address with id=%s", address.id)

        db.delete(address)
        db.commit()

        logger.info("Address deleted successfully with id=%s", address.id)

    @staticmethod
    def get_nearby_addresses(
        db: Session,
        latitude: float,
        longitude: float,
        max_distance_km: float,
    ) -> list[dict]:
        logger.info(
            "Searching nearby addresses for lat=%s lon=%s within %s km",
            latitude,
            longitude,
            max_distance_km,
        )

        addresses = db.query(Address).all()
        nearby_results: list[dict] = []

        for address in addresses:
            distance_km = calculate_distance_km(
                latitude,
                longitude,
                address.latitude,
                address.longitude,
            )

            if distance_km <= max_distance_km:
                nearby_results.append(
                    {
                        "id": address.id,
                        "name": address.name,
                        "latitude": address.latitude,
                        "longitude": address.longitude,
                        "distance_km": round(distance_km, 2),
                        "created_at": address.created_at,
                        "updated_at": address.updated_at,
                    }
                )

        nearby_results.sort(key=lambda item: item["distance_km"])

        logger.info("Found %s nearby addresses", len(nearby_results))
        return nearby_results