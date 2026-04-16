# feature_extractor.py
import time
import numpy as np
import math
from collections import Counter

# ---------- DEVICE RANGES (from your dataset generator) ----------
DEVICE_PACKET_SIZE_RANGES = {
    "camera": (800, 1500),
    "thermostat": (40, 80),
    "smart_bulb": (50, 120),
    "door_lock": (60, 150),
    "smoke_sensor": (40, 100),
    "fan_controller": (80, 200),
    "smart_plug": (60, 150),
    "weather_station": (80, 200),
    "water_meter": (50, 120),
    "energy_meter": (70, 180),
}

# General synthetic bounds (safe clamps derived from generator logic)
CLAMPS = {
    "iat_min": 0.00001,
    "iat_max": 200.0,
    "flow_duration_min": 0.001,
    "flow_duration_max": 200.0,
    "packet_rate_max": 500.0,
    "byte_rate_max": 1e6,
    "entropy_max": 6.0,
}

def calculate_entropy(values):
    if len(values) == 0:
        return 0.0
    counts = Counter(values)
    total = len(values)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())

def _clip_to_device_packet_range(device_type, val):
    rng = DEVICE_PACKET_SIZE_RANGES.get(device_type)
    if not rng:
        rng = DEVICE_PACKET_SIZE_RANGES["camera"]
    lo, hi = rng
    try:
        v = int(val)
    except Exception:
        v = lo
    return max(lo, min(v, hi))

def _clamp(x, lo, hi):
    if x is None:
        return lo
    return max(lo, min(x, hi))

def extract_features(flow_id, packets):
    """
    Convert a pyshark flow into the 21 features expected by your model.
    flow_id = (src_ip, dst_ip, src_port, dst_port, protocol)
    """
    src_ip, dst_ip, src_port, dst_port, protocol = flow_id

    DEVICE_IP_MAP = {
        "192.168.10.2": "camera",
        "192.168.10.3": "thermostat",
        "192.168.10.4": "door_lock",
        "192.168.10.5": "smart_bulb",
        "192.168.10.6": "smoke_sensor",
        "192.168.10.7": "fan_controller",
        "192.168.10.8": "smart_plug",
        "192.168.10.9": "weather_station",
        "192.168.10.10": "water_meter",
        "192.168.10.11": "energy_meter",
    }
    # Get src_ip normally

# DEFAULT
    device_type = "camera"

# Try reading device_type embedded inside UDP payload
    try:
        raw_payload = bytes.fromhex(packets[0].udp.payload.replace(":", ""))
        decoded = raw_payload.decode(errors="ignore")

        if '"device_type"' in decoded:
            import json
            parsed = json.loads(decoded)
            device_type = parsed.get("device_type", "camera")
    except Exception:
        pass

    packet_sizes = []
    timestamps = []
    dest_ports = []

    syn_count = 0
    ack_count = 0
    rst_count = 0

    # Extract raw values defensively
    for pkt in packets:
        try:
            length = getattr(pkt, "length", None)
            if length is not None:
                packet_sizes.append(int(length))
        except Exception:
            pass

        try:
            ts = getattr(pkt, "sniff_timestamp", None)
            if ts is not None:
                timestamps.append(float(ts))
        except Exception:
            pass

        try:
            layer = getattr(pkt, "transport_layer", None)
            if layer and hasattr(pkt, layer):
                dst = getattr(getattr(pkt, layer), "dstport", None)
                if dst is not None:
                    try:
                        dest_ports.append(int(dst))
                    except Exception:
                        pass
        except Exception:
            pass

        # TCP flags extraction (safe)
        try:
            if protocol and str(protocol).upper() == "TCP":
                tcp_layer = getattr(pkt, "tcp", None)
                if tcp_layer is not None:
                    flags = getattr(tcp_layer, "flags", None)
                    if flags is not None:
                        fl = str(flags)
                        if "S" in fl: syn_count += 1
                        if "A" in fl: ack_count += 1
                        if "R" in fl: rst_count += 1
        except Exception:
            pass

    packet_count = len(packet_sizes)
    byte_count = sum(packet_sizes) if packet_sizes else 0

    raw_packet_size = packet_sizes[-1] if packet_count else np.mean(DEVICE_PACKET_SIZE_RANGES[device_type])
    packet_size = _clip_to_device_packet_range(device_type, raw_packet_size)

    avg_packet_size = float(np.mean(packet_sizes)) if packet_count else float(packet_size)

    # timestamps => flow duration and IATs
    if len(timestamps) >= 2:
        start_ts = timestamps[0]
        end_ts = timestamps[-1]
        flow_duration = end_ts - start_ts
        if flow_duration <= 0:
            flow_duration = CLAMPS["flow_duration_min"]
        iat_list = np.diff(timestamps)
        avg_iat = float(np.mean(iat_list)) if len(iat_list) > 0 else CLAMPS["iat_min"]
        inter_arrival_time = float(iat_list[-1]) if len(iat_list) > 0 else CLAMPS["iat_min"]
    elif len(timestamps) == 1:
        flow_duration = CLAMPS["flow_duration_min"]
        avg_iat = CLAMPS["iat_min"]
        inter_arrival_time = CLAMPS["iat_min"]
    else:
        flow_duration = CLAMPS["flow_duration_min"]
        avg_iat = CLAMPS["iat_min"]
        inter_arrival_time = CLAMPS["iat_min"]

    flow_duration = _clamp(flow_duration, CLAMPS["flow_duration_min"], CLAMPS["flow_duration_max"])
    avg_iat = _clamp(avg_iat, CLAMPS["iat_min"], CLAMPS["iat_max"])
    inter_arrival_time = _clamp(inter_arrival_time, CLAMPS["iat_min"], CLAMPS["iat_max"])

    byte_rate = (byte_count / flow_duration) if flow_duration > 0 else 0.0
    byte_rate = _clamp(byte_rate, 0.0, CLAMPS["byte_rate_max"])

    packet_rate_1s = (packet_count / flow_duration) if flow_duration > 0 else 0.0
    packet_rate_1s = _clamp(packet_rate_1s, 0.0, CLAMPS["packet_rate_max"])

    packet_rate_60s = packet_rate_1s * 60.0
    packet_rate_z = (packet_rate_1s - 10.0) / 5.0

    unique_dest_ports = len(set(dest_ports))
    unique_dest_ips = 1

    dest_port_entropy = calculate_entropy(dest_ports)
    dest_port_entropy = _clamp(dest_port_entropy, 0.0, CLAMPS["entropy_max"])

    proto_str = str(protocol).upper() if protocol is not None else ""
    mqtt_ports_present = any(p in (1883, 8883) for p in dest_ports)
    if proto_str == "TCP":
        protocol_id = 2 if mqtt_ports_present else 0
    elif proto_str == "UDP":
        protocol_id = 1
    else:
        protocol_id = 1

    try:
        dp = int(dst_port) if dst_port is not None else None
    except Exception:
        dp = None

    if dp in (80, 443):
        dest_port_bucket = "well_known"
    elif dp in (1883, 8883):
        dest_port_bucket = "iot_service"
    elif dp is not None and dp > 1024:
        dest_port_bucket = "ephemeral"
    else:
        dest_port_bucket = "registered"

    features = {
        "device_type": device_type,
        "timestamp": timestamps[-1] if len(timestamps) > 0 else time.time(),
        "packet_size": int(packet_size),
        "avg_packet_size": float(avg_packet_size),
        "inter_arrival_time": float(inter_arrival_time),
        "avg_iat": float(avg_iat),
        "protocol_id": int(protocol_id),
        "dest_port_bucket": dest_port_bucket,
        "flow_duration": float(flow_duration),
        "packet_count": int(packet_count),
        "byte_rate": float(byte_rate),
        "packet_rate_1s": float(packet_rate_1s),
        "packet_rate_60s": float(packet_rate_60s),
        "packet_rate_z": float(packet_rate_z),
        "unique_dest_ports_count": int(unique_dest_ports),
        "unique_dest_ips_count": int(unique_dest_ips),
        "dest_port_entropy": float(dest_port_entropy),
        "syn_flag_count": int(syn_count),
        "ack_flag_count": int(ack_count),
        "rst_flag_count": int(rst_count)
    }

    return features
