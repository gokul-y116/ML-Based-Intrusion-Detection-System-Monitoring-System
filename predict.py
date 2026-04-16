import pickle
import numpy as np

# Load artifacts
with open("iot_rf_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    encoders = pickle.load(f)


# The features in correct order (must match training EXACTLY)
FEATURE_ORDER = [
    "device_type",
    "packet_size",
    "avg_packet_size",
    "inter_arrival_time",
    "avg_iat",
    "protocol_id",
    "dest_port_bucket",
    "flow_duration",
    "packet_count",
    "byte_rate",
    "packet_rate_1s",
    "packet_rate_60s",
    "packet_rate_z",
    "unique_dest_ports_count",
    "unique_dest_ips_count",
    "dest_port_entropy",
    "syn_flag_count",
    "ack_flag_count",
    "rst_flag_count"
]


def preprocess_input(feature_dict):
    """Convert raw gateway features into model-ready vector."""

    processed = []

    for key in FEATURE_ORDER:

        val = feature_dict[key]

        # Encode categorical features
        if key in ("device_type", "dest_port_bucket"):
            encoder = encoders[key]
            val = encoder.transform([val])[0]

        processed.append(val)

    processed = np.array(processed).reshape(1, -1)

    # Scale numeric values
    processed = scaler.transform(processed)

    return processed


def predict_attack(features):
    """Take 21-feature dict → return prediction + confidence."""

    X = preprocess_input(features)
    y_pred = model.predict(X)[0]

    # For confidence: take probability of predicted class
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        conf = float(np.max(probs))
    else:
        conf = 1.0

    return {
        "attack_type": y_pred,
        "confidence": conf
    }
