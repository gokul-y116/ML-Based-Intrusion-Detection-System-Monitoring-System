import socket, json, time
from shared_features import generate_features

GATEWAY_IP = "192.168.118.23"
GATEWAY_PORT = 5000
DEVICE_IP = "192.168.10.4"
DEVICE_TYPE = "smart_bulb"
INTERVAL = 1.5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"[STARTED] SMART BULB sending → {GATEWAY_IP}:{GATEWAY_PORT}")

while True:
    f = generate_features(DEVICE_TYPE)
    f["device_type"] = DEVICE_TYPE
    f["src_ip"] = DEVICE_IP

    sock.sendto(json.dumps(f).encode(), (GATEWAY_IP, GATEWAY_PORT))
    print(f)
    time.sleep(INTERVAL)
