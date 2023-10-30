from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel, PositiveFloat

# See
# https://www.datacaptains.com/blog/building-and-load-testing-a-machine-learning-service
# for more info on this model.
ML_MODEL = joblib.load("./model.joblib")

# FastAPI.
api_title = "RealEstateUnitPriceApp"
api_description = """
RealEstateUnitPriceApp allows you to predict the unit price of real estate
in New Taipei City, Taiwan on the basis of the distance of the property from
the closest station of the Mass Rapid Transit (MRT).
"""
api = FastAPI(title=api_title, description=api_description)


class Distance(BaseModel):
    """
    Data model for distance.
    """

    Distance: PositiveFloat


class UnitPrice(BaseModel):
    """
    Data model for unit price.
    """

    # Our simple linear regression model does not make only positive
    # predictions. So, technically, we can only guarantee that we will return
    # a float. We can't guarantee it will be a PositiveFloat.
    UnitPrice: float


def predict(log_distance: float) -> float:
    """
    Utility to make predictions from the ML model.
    """
    return ML_MODEL.predict(np.array([[log_distance]]))[0]


@api.post("/unitprice", response_model=UnitPrice)
def unit_price(distance: Distance) -> UnitPrice:
    """
    Predicts the unit price of real estate (in 10,000 New Taiwan Dollars
    per Ping) based on the distance (in meters) from the closest Mass
    Rapid Transit station.
    """
    log_distance = np.log(distance.Distance)
    unit_price = predict(log_distance)
    return UnitPrice(UnitPrice=unit_price)
