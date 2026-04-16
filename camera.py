# camera.py
import socket
import json
import time
from shared_features import generate_features

GATEWAY_IP = "192.168.118.23"
GATEWAY_PORT = 5000
DEVICE_IP = "192.168.10.2"
DEVICE_TYPE = "camera"
INTERVAL = 1   # seconds per flow

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"[STARTED] CAMERA sending traffic → {GATEWAY_IP}:{GATEWAY_PORT}")

while True:
    features = generate_features(DEVICE_TYPE)
    features["device_type"] = DEVICE_TYPE
    features["src_ip"] = DEVICE_IP

    sock.sendto(json.dumps(features).encode(), (GATEWAY_IP, GATEWAY_PORT))

    print(f"Sent: {features}")
    time.sleep(INTERVAL)
