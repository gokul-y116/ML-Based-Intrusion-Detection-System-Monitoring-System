# flowBuilder.py
import time

# flow_id → { start_time, packets }
flows = {}

FLOW_TIMEOUT = 1  # seconds; close flow if idle for >= 1s

def get_flow_id(packet):
    """Create a unique ID for each flow."""
    try:
        src_ip = packet.ip.src
    except Exception:
        src_ip = getattr(packet, "source", None)

    try:
        dst_ip = packet.ip.dst
    except Exception:
        dst_ip = getattr(packet, "destination", None)

    src_port = None
    dst_port = None
    try:
        layer = getattr(packet, "transport_layer", None)
        if layer and hasattr(packet, layer):
            src_port = getattr(getattr(packet, layer), "srcport", None)
            dst_port = getattr(getattr(packet, layer), "dstport", None)
    except Exception:
        src_port = None
        dst_port = None

    protocol = getattr(packet, "transport_layer", None)

    return (src_ip, dst_ip, src_port, dst_port, protocol)

def add_packet_to_flow(packet):
    """Add packet to the appropriate flow."""
    flow_id = get_flow_id(packet)

    if flow_id not in flows:
        flows[flow_id] = {
            "start_time": time.time(),
            "packets": []
        }

    flows[flow_id]["packets"].append(packet)
    # update last-seen time to keep flow alive
    flows[flow_id]["start_time"] = flows[flow_id].get("start_time", time.time())

def extract_completed_flows():
    """Return flows that have exceeded timeout."""
    completed = []
    now = time.time()

    for fid, data in list(flows.items()):
        if now - data["start_time"] >= FLOW_TIMEOUT:
            completed.append((fid, data["packets"]))
            del flows[fid]

    return completed
