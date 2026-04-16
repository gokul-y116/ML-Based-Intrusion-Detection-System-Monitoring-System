# attack_profiles.py
import random

def ddos_flood(device):
    packet_size = random.randint(60, 120)
    iat = round(random.uniform(0.00001, 0.005), 6)
    duration = random.uniform(0.01, 0.2)
    pkt_count = random.randint(50, 300)

    return {
        "packet_size": packet_size,
        "avg_packet_size": packet_size,
        "inter_arrival_time": iat,
        "avg_iat": iat,
        "protocol_id": 1,
        "dest_port_bucket": "ephemeral",
        "flow_duration": duration,
        "packet_count": pkt_count,
        "byte_rate": round((packet_size * pkt_count) / duration, 3),
        "packet_rate_1s": pkt_count,
        "packet_rate_60s": pkt_count * random.randint(20, 50),
        "packet_rate_z": round((pkt_count - 10)/5, 3),
        "unique_dest_ports_count": random.randint(1, 5),
        "unique_dest_ips_count": random.randint(1, 5),
        "dest_port_entropy": round(random.uniform(0.1, 1.5), 3),
        "syn_flag_count": 0,
        "ack_flag_count": 0,
        "rst_flag_count": random.randint(0, 3),
        "window_label": 1
    }

def syn_flood(device):
    packet_size = random.randint(40, 60)
    iat = round(random.uniform(0.0001, 0.003), 5)
    duration = random.uniform(0.01, 0.1)
    pkt_count = random.randint(30, 200)
    syn = random.randint(100, 500)

    return {
        "packet_size": packet_size,
        "avg_packet_size": packet_size,
        "inter_arrival_time": iat,
        "avg_iat": iat,
        "protocol_id": 0,
        "dest_port_bucket": "well_known",
        "flow_duration": duration,
        "packet_count": pkt_count,
        "byte_rate": round((packet_size * pkt_count)/duration, 3),
        "packet_rate_1s": pkt_count,
        "packet_rate_60s": pkt_count * random.randint(10, 30),
        "packet_rate_z": round((pkt_count - 10)/5, 3),
        "unique_dest_ports_count": random.randint(1, 5),
        "unique_dest_ips_count": random.randint(1, 5),
        "dest_port_entropy": round(random.uniform(0.5, 2.0), 3),
        "syn_flag_count": syn,
        "ack_flag_count": 0,
        "rst_flag_count": 0,
        "window_label": 1
    }

def udp_flood(device):
    packet_size = random.randint(500, 1200)
    iat = round(random.uniform(0.0001, 0.003), 5)
    duration = random.uniform(0.01, 0.1)
    pkt_count = random.randint(50, 250)

    return {
        "packet_size": packet_size,
        "avg_packet_size": packet_size,
        "inter_arrival_time": iat,
        "avg_iat": iat,
        "protocol_id": 1,
        "dest_port_bucket": "ephemeral",
        "flow_duration": duration,
        "packet_count": pkt_count,
        "byte_rate": round((packet_size * pkt_count)/duration, 3),
        "packet_rate_1s": pkt_count,
        "packet_rate_60s": pkt_count * random.randint(15, 40),
        "packet_rate_z": round((pkt_count - 10)/5, 3),
        "unique_dest_ports_count": random.randint(1, 5),
        "unique_dest_ips_count": random.randint(1, 5),
        "dest_port_entropy": round(random.uniform(0.3, 1.8), 3),
        "syn_flag_count": 0,
        "ack_flag_count": 0,
        "rst_flag_count": 0,
        "window_label": 1
    }

def slowloris(device):
    packet_size = random.randint(10, 40)
    iat = round(random.uniform(10, 30), 3)
    duration = random.uniform(60, 200)
    pkt_count = random.randint(1, 3)
    syn = random.randint(1, 3)

    return {
        "packet_size": packet_size,
        "avg_packet_size": packet_size,
        "inter_arrival_time": iat,
        "avg_iat": iat,
        "protocol_id": 0,
        "dest_port_bucket": "well_known",
        "flow_duration": duration,
        "packet_count": pkt_count,
        "byte_rate": round((packet_size * pkt_count)/duration, 3),
        "packet_rate_1s": pkt_count,
        "packet_rate_60s": pkt_count * random.randint(1, 5),
        "packet_rate_z": round((pkt_count - 10)/5, 3),
        "unique_dest_ports_count": random.randint(1, 3),
        "unique_dest_ips_count": random.randint(1, 3),
        "dest_port_entropy": round(random.uniform(0.2, 1.2), 3),
        "syn_flag_count": syn,
        "ack_flag_count": 0,
        "rst_flag_count": 0,
        "window_label": 1
    }
