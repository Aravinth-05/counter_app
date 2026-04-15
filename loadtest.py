"""
loadtest.py -- Generate traffic on the Counter API

Sends a mix of requests to all endpoints to simulate real usage.
Run this while watching Datadog to see:
  - Request rate spike
  - Latency per endpoint
  - Traffic distribution across the 2 API pods

Usage:
  python loadtest.py
"""

import requests
import time
import random
import sys

# If running inside K8s, use the service name.
# If running from your machine, use localhost.
API_URL = "http://localhost:8000"

ENDPOINTS = [
    ("GET", "/counter"),
    ("POST", "/counter/increment"),
    ("POST", "/counter/increment"),
    ("POST", "/counter/increment"),
    ("POST", "/counter/decrement"),
    ("POST", "/counter/reset"),
    ("GET", "/health"),
]

TOTAL_REQUESTS = 500
REQUESTS_PER_SECOND = 10


def run():
    print(f"Sending {TOTAL_REQUESTS} requests to {API_URL}")
    print(f"Rate: ~{REQUESTS_PER_SECOND} requests/second")
    print("-" * 50)

    success = 0
    errors = 0
    start = time.time()

    for i in range(TOTAL_REQUESTS):
        method, path = random.choice(ENDPOINTS)
        url = f"{API_URL}{path}"

        try:
            if method == "GET":
                resp = requests.get(url, timeout=5)
            else:
                resp = requests.post(url, timeout=5)

            if resp.status_code == 200:
                success += 1
            else:
                errors += 1
                print(f"  [{resp.status_code}] {method} {path}")

        except Exception as e:
            errors += 1
            print(f"  [ERROR] {method} {path} -- {e}")

        # Progress update every 50 requests
        if (i + 1) % 50 == 0:
            elapsed = time.time() - start
            print(f"  Sent {i + 1}/{TOTAL_REQUESTS} requests ({elapsed:.1f}s elapsed)")

        # Throttle to target rate
        time.sleep(1 / REQUESTS_PER_SECOND)

    elapsed = time.time() - start
    print("-" * 50)
    print(f"Done in {elapsed:.1f}s")
    print(f"  Success: {success}")
    print(f"  Errors:  {errors}")
    print(f"  Rate:    {TOTAL_REQUESTS / elapsed:.1f} req/s")
    print()
    print("Now check Datadog:")
    print("  APM:    https://ap1.datadoghq.com/apm/services")
    print("  Traces: https://ap1.datadoghq.com/apm/traces")
    print("  Infra:  https://ap1.datadoghq.com/containers")


if __name__ == "__main__":
    run()
