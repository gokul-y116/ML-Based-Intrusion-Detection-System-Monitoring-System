import socket, json, time
from attack_profiles import udp_flood

GATEWAY_IP = "192.168.118.23"
GATEWAY_PORT = 5000
DEVICE_TYPE = "thermostat"
ATTACK_IP = "192.168.10.3"
INTERVAL = 0.15

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("[STARTED] UDP FLOOD attack from camera")

while True:
    f = udp_flood(DEVICE_TYPE)
    f["device_type"] = DEVICE_TYPE
    f["src_ip"] = ATTACK_IP
    f["timestamp"] = time.time()

    sock.sendto(json.dumps(f).encode(), (GATEWAY_IP, GATEWAY_PORT))
    print("UDP FLOOD:", f)
    time.sleep(INTERVAL)
