import joblib
import pandas as pd
import numpy as np

# -----------------------
# Load model + utilities
# -----------------------
model = joblib.load("iot_rf_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
scaler = joblib.load("scaler.pkl")

print("Artifacts Loaded Successfully!")


def predict_flow(data_dict):
    """
    Takes 1 flow of data as a dictionary and returns predicted label.
    """

    df = pd.DataFrame([data_dict])

    # -----------------------
    # Apply Label Encoders
    # -----------------------
    for col in label_encoders:
        df[col] = label_encoders[col].transform(df[col])

    # -----------------------
    # Scale numeric features
    # -----------------------
    df_scaled = scaler.transform(df)

    # -----------------------
    # Predict
    # -----------------------
    prediction = model.predict(df_scaled)[0]

    return prediction


# -----------------------
# DEMO RUN
# -----------------------
if __name__ == "__main__":
    sample = {
        "device_type": "camera",
        "packet_size": 450,
        "avg_packet_size": 300,
        "inter_arrival_time": 0.0021,
        "avg_iat": 0.003,
        "protocol_id": 6,
        "dest_port_bucket": 2,
        "flow_duration": 1.24,
        "packet_count": 23,
        "byte_rate": 3412,
        "packet_rate_1s": 10,
        "packet_rate_60s": 80,
        "packet_rate_z": 1.1,
        "unique_dest_ports_count": 3,
        "unique_dest_ips_count": 1,
        "dest_port_entropy": 0.22,
        "syn_flag_count": 0,
        "ack_flag_count": 5,
        "rst_flag_count": 0
    }

    result = predict_flow(sample)
    print("Prediction:", result)
