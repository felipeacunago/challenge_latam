import fastapi
from challenge.model import DelayModel
import pandas as pd

app = fastapi.FastAPI()

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(payload : dict) -> dict:
    model = DelayModel()
    preprocessed_data = model.preprocess(pd.DataFrame(payload["flights"]))
    return {"predict": model.predict(preprocessed_data)}