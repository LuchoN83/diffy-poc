import time
import requests
import random

BASE = "http://nginx:80"

ENDPOINTS = ["/success", "/regression", "/noise"]

def main():
    print("Generating traffic to NGINX (legacy + mirrored to Diffy)...")
    for i in range(300):
        ep = random.choice(ENDPOINTS)
        try:
            r = requests.get(BASE + ep, timeout=2)
            if i % 25 == 0:
                print(f"[{i}] GET {ep} -> {r.status_code}")
        except Exception as e:
            print(f"Error calling {ep}: {e}")
        time.sleep(0.05)

    print("Done. Let Diffy process comparisons for a few seconds...")
    time.sleep(5)

if __name__ == "__main__":
    main()
