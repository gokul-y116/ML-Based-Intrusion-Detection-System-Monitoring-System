import socket, json, time, random

GATEWAY_IP = "192.168.118.23"
GATEWAY_PORT = 5000
ATTACK_IP = "192.168.10.8"

def botnet_beacon():
    size = random.randint(40, 60)
    iat = random.uniform(20, 60)
    pkt_count = random.randint(1, 2)

    return {
        "packet_size": size,
        "avg_packet_size": size,
        "inter_arrival_time": iat,
        "avg_iat": iat,
        "protocol_id": 2,
        "dest_port_bucket": "iot_service",
        "flow_duration": random.uniform(1,3),
        "packet_count": pkt_count,
        "byte_rate": 20,
        "packet_rate_1s": pkt_count,
        "packet_rate_60s": pkt_count*5,
        "packet_rate_z": -1,
        "unique_dest_ports_count": 1,
        "unique_dest_ips_count": random.randint(1,3),
        "dest_port_entropy": random.uniform(0.2, 1.2),
        "syn_flag_count": 0,
        "ack_flag_count": 0,
        "rst_flag_count": 0,
        "window_label": 1
    }

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("[STARTED] BOTNET BEACON attack")

while True:
    f = botnet_beacon()
    f["device_type"] = "smart_plug"
    f["src_ip"] = ATTACK_IP
    f["timestamp"] = time.time()

    sock.sendto(json.dumps(f).encode(), (GATEWAY_IP, GATEWAY_PORT))
    print("BOTNET BEACON:", f)

    time.sleep(5)
