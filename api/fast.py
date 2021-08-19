from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import numpy as np
import pandas as pd
import pytz
import joblib

PATH_TO_LOCAL_MODEL = 'model.joblib'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

# create a datetime object from the user provided datetime
pickup_datetime = "2021-05-30 10:12:00"
pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

# localize the user datetime with NYC timezone
eastern = pytz.timezone("US/Eastern")
localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)


@app.get("/predict")
def predict(pickup_datetime, pickup_longitude, pickup_latitude,
            dropoff_longitude, dropoff_latitude, passenger_count):

    # compute `wait_prediction` from `day_of_week` and `time`

    # create a datetime object from the user provided datetime
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)

    formatted_pickup_datetime = localized_pickup_datetime.strftime(
        "%Y-%m-%d %H:%M:%S UTC")

    dico = {
        "key": "2013-07-06 17:18:00.000000119",
        "pickup_datetime": formatted_pickup_datetime,
        "pickup_longitude": float(pickup_longitude),
        "pickup_latitude": float(pickup_latitude),
        "dropoff_longitude": float(dropoff_longitude),
        "dropoff_latitude": float(dropoff_latitude),
        "passenger_count": int(passenger_count)
    }

    pipeline = joblib.load(PATH_TO_LOCAL_MODEL)
    #array = np.array(dico)
    X_test = pd.DataFrame(dico,index=[0])
    #X_test.reindex('keys')
    pred = pipeline.predict(X_test)
    output={'prediction' : round(pred[0],2)}

    return output


if __name__=='__main__':

    predict('2013-07-06 17:18:00', '-73.950655', '40.783282', '-73.984365',
            '40.769802', '1')

# class Item(parent_class):
#     name: str
#     description: str = None
#     price: float
#     tax: float = None


# @app.post("/items/")
# async def create_item(item: Item):
#     return item
