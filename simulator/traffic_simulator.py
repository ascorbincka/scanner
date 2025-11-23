import random
import time
import requests
from datetime import datetime

BACKEND_EVENTS_URL = "http://127.0.0.1:8000/events"

ATTACK_IPS = [
    "10.0.0.10",
    "10.0.0.11",
    "10.0.0.12",
]

NORMAL_IPS = [
    "192.168.0.5",
    "192.168.0.6",
]

DEST_IPS = [
    "192.168.1.10",
    "192.168.1.20",
]

PORTS = [22, 80, 443, 21, 25, 8080, 3389]


def generate_event():
    is_attack = random.random() < 0.7  # 70% "атак" 30% норм

    if is_attack:
        src_ip = random.choice(ATTACK_IPS)
    else:
        src_ip = random.choice(NORMAL_IPS)

    dest_ip = random.choice(DEST_IPS)
    dest_port = random.choice(PORTS)

    event = {
        "source_ip": src_ip,
        "dest_ip": dest_ip,
        "dest_port": dest_port,
        "protocol": "TCP",
        "timestamp": datetime.utcnow().isoformat(),
    }
    return event


def main_loop():
    while True:
        event = generate_event()
        try:
            resp = requests.post(BACKEND_EVENTS_URL, json=event, timeout=2)
            print(f"Sent event: {event} -> status={resp.status_code} {resp.text}")
        except Exception as e:
            print(f"Error sending event: {e}")

        time.sleep(0.5)


if __name__ == "__main__":
    main_loop()
