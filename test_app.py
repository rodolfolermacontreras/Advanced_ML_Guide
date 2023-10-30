from fastapi.testclient import TestClient

from app import api, UnitPrice

client = TestClient(api)


def test_unit_price(mocker):
    # Arrange.
    request_body = {"Distance": 123.4}
    mocker.patch("app.predict", return_value=56.7)  # this requires pytest-mock

    # Act.
    response = client.post("/unitprice", json=request_body)

    # Assert.
    assert response.status_code == 200
    assert response.json() == UnitPrice(UnitPrice=56.7).model_dump()
