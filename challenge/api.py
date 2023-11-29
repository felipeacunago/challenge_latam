import fastapi
from pydantic import BaseModel
from challenge.model import DelayModel
import pandas as pd
from fastapi.responses import JSONResponse

# validation using pydantic
from pydantic import BaseModel, validator
from typing import List

# exceptions
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

app = fastapi.FastAPI()

# Flight type
class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

    @validator('MES')
    def validate_month(cls, v):
        if v < 1 or v > 12:
            raise ValueError('Month should be a value between 1 and 12')
        return v

# as the payload contains an array of features data, it will be parsed as a list
class RequestBody(BaseModel):
    flights: List[Flight]

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: fastapi.Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(payload : RequestBody) -> dict:
    model = DelayModel()
    preprocessed_data = model.preprocess(pd.DataFrame(payload.dict()['flights']))
    return {"predict": model.predict(preprocessed_data)}