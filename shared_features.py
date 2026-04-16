# shared_features.py
import random
import time
from datetime import datetime, timedelta

# --------------------------------------------
# MATCHES EXACT LOGIC IN DATASET GENERATOR
# --------------------------------------------

def choose_protocol(device):
    if device in ["thermostat", "smart_bulb", "smoke_sensor", "water_meter"]:
        return 2  # MQTT
    if device == "camera":
        return random.choice([0, 1])
    return random.choice([0, 1, 2])

def port_bucket(device):
    if device in ["thermostat", "smart_bulb", "smoke_sensor", "water_meter"]:
        return "iot_service"
    return random.choice(["well_known", "registered", "ephemeral"])

def device_packet_range(device):
    ranges = {
        "camera": (800, 1500),
        "thermostat": (40, 80),
        "smart_bulb": (50, 120),
        "door_lock": (60, 150),
        "smoke_sensor": (40, 100),
        "fan_controller": (80, 200),
        "smart_plug": (60, 150),
        "weather_station": (80, 200),
        "water_meter": (50, 120),
        "energy_meter": (70, 180)
    }
    return ranges[device]

def generate_features(device):

    # Base device ranges
    pmin, pmax = device_packet_range(device)
    packet_size = random.randint(pmin, pmax)

    iat = round(random.uniform(0.5, 5.0), 4)
    duration = round(random.uniform(0.2, 2.0), 3)
    pkt_count = random.randint(1, 8)
    protocol = choose_protocol(device)
    bucket = port_bucket(device)

    # TCP flags
    syn = ack = rst = 0
    if protocol == 0:  # TCP normal behavior
        ack = random.randint(1, pkt_count)
        syn = 1 if random.random() < 0.1 else 0

    avg_packet = packet_size
    avg_iat = iat
    byte_rate = round((packet_size * pkt_count) / max(duration, 0.001), 3)

    pr1 = pkt_count
    pr60 = pkt_count * random.randint(5, 40)
    pr_z = round((pr1 - 10) / 5, 3)

    port_div = random.randint(1, 10)
    ip_div = random.randint(1, 8)
    entropy = round(random.uniform(0.1, 3.5), 3)

    return {
        "timestamp": time.time(),
        "packet_size": packet_size,
        "avg_packet_size": avg_packet,
        "inter_arrival_time": iat,
        "avg_iat": avg_iat,
        "protocol_id": protocol,
        "dest_port_bucket": bucket,
        "flow_duration": duration,
        "packet_count": pkt_count,
        "byte_rate": byte_rate,
        "packet_rate_1s": pr1,
        "packet_rate_60s": pr60,
        "packet_rate_z": pr_z,
        "unique_dest_ports_count": port_div,
        "unique_dest_ips_count": ip_div,
        "dest_port_entropy": entropy,
        "syn_flag_count": syn,
        "ack_flag_count": ack,
        "rst_flag_count": rst,
        "window_label": 0  # normal traffic
    }
