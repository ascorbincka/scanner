import random
import time
import requests

BACKEND_EVENTS_URL = "http://127.0.0.1:8000/events"  # сюда шлём события

ATTACK_IPS = [
    "10.0.0.10",
    "10.0.0.11",
    "10.0.0.12",
]

NORMAL_IPS = [
    "192.168.0.5",
    "192.168.0.6",
]

PORTS = [22, 80, 443, 21, 25, 8080, 3389]


def generate_event():
    """
    Генерирует одно событие:
    - либо «атакующий» IP с кучей портов,
    - либо нормальный IP с 1–2 портами.
    """
    is_attack = random.random() < 0.7  # 70% атак, 30% нормальный трафик

    if is_attack:
        ip = random.choice(ATTACK_IPS)
        ports = random.sample(PORTS, k=random.randint(3, 6))
        kind = "attack"
    else:
        ip = random.choice(NORMAL_IPS)
        ports = random.sample(PORTS, k=random.randint(1, 2))
        kind = "normal"

    event = {
        "src_ip": ip,
        "ports": ports,
        "kind": kind, 
    }
    return event


def main_loop():
    while True:
        event = generate_event()
        try:
            resp = requests.post(BACKEND_EVENTS_URL, json=event, timeout=2)
            print(f"Sent event: {event} -> status={resp.status_code}")
        except Exception as e:
            print(f"Error sending event: {e}")

        time.sleep(0.5)  # чтобы не спамить 


if __name__ == "__main__":
    main_loop()
