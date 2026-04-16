import socket, json, time
from shared_features import generate_features

GATEWAY_IP = "192.168.118.23"
GATEWAY_PORT = 5000
DEVICE_IP = "192.168.10.3"
DEVICE_TYPE = "thermostat"
INTERVAL = 1.2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"[STARTED] THERMOSTAT sending → {GATEWAY_IP}:{GATEWAY_PORT}")

while True:
    f = generate_features(DEVICE_TYPE)
    f["device_type"] = DEVICE_TYPE
    f["src_ip"] = DEVICE_IP

    sock.sendto(json.dumps(f).encode(), (GATEWAY_IP, GATEWAY_PORT))
    print(f)
    time.sleep(INTERVAL)
