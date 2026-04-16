import socket, json, time
from attack_profiles import ddos_flood

GATEWAY_IP = "192.168.118.23"
GATEWAY_PORT = 5000
DEVICE_TYPE = "energy_meter"
ATTACK_IP = "192.168.10.11"
INTERVAL = 0.1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("[STARTED] DDoS FLOOD attack from camera")

while True:
    f = ddos_flood(DEVICE_TYPE)
    f["device_type"] = DEVICE_TYPE
    f["src_ip"] = ATTACK_IP
    f["timestamp"] = time.time()

    sock.sendto(json.dumps(f).encode(), (GATEWAY_IP, GATEWAY_PORT))
    print("DDoS FLOOD:", f)
    time.sleep(INTERVAL)
