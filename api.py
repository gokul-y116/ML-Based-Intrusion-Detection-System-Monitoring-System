from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import time

# ------------------------------
# Load model & preprocessors
# ------------------------------
MODEL_DIR = "../models"

model = joblib.load(os.path.join(MODEL_DIR, "iot_rf_model.pkl"))
encoders = joblib.load(os.path.join(MODEL_DIR, "label_encoders.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

app = FastAPI(title="IoT Intrusion Detection API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------
# In-Memory Log Storage (for Dashboard)
# ------------------------------
EVENT_LOG = []   # Stores device_type, timestamp, status

# ------------------------------
# 21 Features Expected
# ------------------------------
class FlowInput(BaseModel):
    device_type: str
    timestamp: float
    packet_size: float
    avg_packet_size: float
    inter_arrival_time: float
    avg_iat: float
    protocol_id: int
    dest_port_bucket: str
    flow_duration: float
    packet_count: int
    byte_rate: float
    packet_rate_1s: float
    packet_rate_60s: float
    packet_rate_z: float
    unique_dest_ports_count: int
    unique_dest_ips_count: int
    dest_port_entropy: float
    syn_flag_count: int
    ack_flag_count: int
    rst_flag_count: int

# ------------------------------
# Prediction Route
# ------------------------------
@app.post("/predict")
def predict_flow(data: FlowInput):

    df = pd.DataFrame([data.dict()])

    # Encode categorical columns
    df["device_type"] = encoders["device_type"].transform(df["device_type"])
    df["dest_port_bucket"] = encoders["dest_port_bucket"].transform(df["dest_port_bucket"])

    # Scale numerics
    df_scaled = scaler.transform(df)

    # Model prediction
    pred = model.predict(df_scaled)[0]
    status = "NORMAL" if pred == 0 else "ATTACK DETECTED"

    # ------------------------------
    # SAVE EVENT FOR DASHBOARD
    # ------------------------------
    EVENT_LOG.append({
        "timestamp": data.timestamp,
        "device_type": data.device_type,
        "status": status
    })

    # keep memory small
    if len(EVENT_LOG) > 500:
        EVENT_LOG.pop(0)

    return {
        "prediction": int(pred),
        "status": status
    }

# ------------------------------
# Dashboard Events Route
# ------------------------------
@app.get("/events")
def get_events():
    return EVENT_LOG
