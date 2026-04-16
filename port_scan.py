import socket, json, time
import random

GATEWAY_IP = "192.168.118.23"
GATEWAY_PORT = 5000
ATTACK_IP = "192.168.10.8"

def port_scan():
    syn = random.randint(5, 20)
    packet_size = random.randint(40, 80)
    iat = round(random.uniform(0.01, 0.5), 3)

    return {
        "packet_size": packet_size,
        "avg_packet_size": packet_size,
        "inter_arrival_time": iat,
        "avg_iat": iat,
        "protocol_id": 0,
        "dest_port_bucket": "well_known",
        "flow_duration": random.uniform(0.1, 1.0),
        "packet_count": random.randint(1, 5),
        "byte_rate": random.uniform(1000, 5000),
        "packet_rate_1s": random.randint(2, 10),
        "packet_rate_60s": random.randint(20, 100),
        "packet_rate_z": -1,
        "unique_dest_ports_count": random.randint(10, 50),
        "unique_dest_ips_count": 1,
        "dest_port_entropy": round(random.uniform(0.8, 2.5), 3),
        "syn_flag_count": syn,
        "ack_flag_count": 0,
        "rst_flag_count": 0,
        "window_label": 1
    }

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("[STARTED] PORT SCAN attack")

while True:
    f = port_scan()
    f["device_type"] = "smart_plug"
    f["src_ip"] = ATTACK_IP
    f["timestamp"] = time.time()

    sock.sendto(json.dumps(f).encode(), (GATEWAY_IP, GATEWAY_PORT))
    print("PORT SCAN:", f)

    time.sleep(0.3)
