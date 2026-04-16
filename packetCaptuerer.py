# packetCaptuerer.py
import pyshark
import time

from flowBuilder import add_packet_to_flow, extract_completed_flows
from feature_extractor import extract_features
from send_to_backend import send_features_to_backend

# -----------------------------------------------------------
# CAPTURE CONFIGURATION
# -----------------------------------------------------------
# This captures BOTH TCP and UDP packets going to port 5000
# (matches your iot.py traffic generator)
BPF_FILTER = "port 5000"

# Change this to match your actual network interface:
# Windows  : "Wi-Fi"
# Linux    : "wlan0"
# Mac      : "en0"
DEFAULT_INTERFACE = "wifi"

# -----------------------------------------------------------
def start_capture(interface=DEFAULT_INTERFACE):
    print("==========================================")
    print("   LIVE PACKET CAPTURE STARTED")
    print("   Interface:", interface)
    print("   Filter   :", BPF_FILTER)
    print("==========================================")

    capture = pyshark.LiveCapture(
        interface=interface,
        bpf_filter=BPF_FILTER
    )

    last_check = time.time()

    try:
        for packet in capture.sniff_continuously():
            try:
                add_packet_to_flow(packet)

                now = time.time()

                # Check for completed flows every 1 sec
                if now - last_check >= 1:
                    completed = extract_completed_flows()

                    for flow_id, pkts in completed:
                        print("\n===== FLOW COMPLETED =====")
                        print("FLOW ID:", flow_id)
                        print("Packets:", len(pkts))

                        # Extract 21 features
                        features = extract_features(flow_id, pkts)

                        if not features:
                            print("⚠ No features extracted, skipping...")
                            continue

                        # Pretty print features
                        print("-- Extracted Features --")
                        for k, v in features.items():
                            print(f"{k}: {v}")

                        # Send to backend
                        prediction = send_features_to_backend(features)

                        print("-- MODEL PREDICTION --")
                        print(prediction)
                        print("==========================\n")

                    last_check = now

            except Exception as e:
                print("⚠ Packet Error:", e)

    except KeyboardInterrupt:
        print("🛑 Capture stopped by user.")

    except Exception as e:
        print("❌ Fatal Error:", e)

    finally:
        capture.close()
        print("Capture session closed.")

# -----------------------------------------------------------
if __name__ == "__main__":
    start_capture()
