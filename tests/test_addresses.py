def test_create_address(client):
    payload = {
        "name": "Home",
        "latitude": 10.8505,
        "longitude": 76.2711,
    }

    response = client.post("/addresses", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Home"
    assert data["latitude"] == 10.8505
    assert data["longitude"] == 76.2711
    assert "created_at" in data
    assert "updated_at" in data


def test_get_address_by_id(client):
    payload = {
        "name": "Office",
        "latitude": 10.8505,
        "longitude": 76.2711,
    }

    create_response = client.post("/addresses", json=payload)
    address_id = create_response.json()["id"]

    response = client.get(f"/addresses/{address_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == address_id
    assert data["name"] == "Office"


def test_get_nonexistent_address_returns_404(client):
    response = client.get("/addresses/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Address not found."}


def test_update_address(client):
    payload = {
        "name": "Old Name",
        "latitude": 10.8505,
        "longitude": 76.2711,
    }

    create_response = client.post("/addresses", json=payload)
    address_id = create_response.json()["id"]

    update_payload = {
        "name": "New Name"
    }

    response = client.patch(f"/addresses/{address_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == address_id
    assert data["name"] == "New Name"
    assert data["latitude"] == 10.8505
    assert data["longitude"] == 76.2711


def test_delete_address(client):
    payload = {
        "name": "To Delete",
        "latitude": 10.8505,
        "longitude": 76.2711,
    }

    create_response = client.post("/addresses", json=payload)
    address_id = create_response.json()["id"]

    delete_response = client.delete(f"/addresses/{address_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/addresses/{address_id}")
    assert get_response.status_code == 404


def test_get_nearby_addresses(client):
    client.post(
        "/addresses",
        json={"name": "Kochi", "latitude": 9.9312, "longitude": 76.2673},
    )
    client.post(
        "/addresses",
        json={"name": "Thrissur", "latitude": 10.5276, "longitude": 76.2144},
    )
    client.post(
        "/addresses",
        json={"name": "Bangalore", "latitude": 12.9716, "longitude": 77.5946},
    )

    response = client.get(
        "/addresses/nearby",
        params={
            "latitude": 9.9312,
            "longitude": 76.2673,
            "distance_km": 100,
        },
    )

    assert response.status_code == 200
    data = response.json()

    names = [item["name"] for item in data]

    assert "Kochi" in names
    assert "Bangalore" not in names


def test_invalid_latitude_returns_422(client):
    payload = {
        "name": "Invalid Place",
        "latitude": 200,
        "longitude": 76.2711,
    }

    response = client.post("/addresses", json=payload)

    assert response.status_code == 422