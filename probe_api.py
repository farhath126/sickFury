import requests

urls = [
    "https://www.gosugamers.net/api/matches",
    "https://www.gosugamers.net/api/v1/matches",
    "https://www.gosugamers.net/counterstrike/matches?format=json",
    "https://www.gosugamers.net/_next/data/build-id/counterstrike/matches.json" # Next.js specific, need build ID
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

for u in urls:
    try:
        print(f"Testing {u}...")
        resp = requests.get(u, headers=headers, timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200 and "application/json" in resp.headers.get("Content-Type", ""):
            print("Found JSON!")
            print(resp.text[:200])
    except Exception as e:
        print(f"Error: {e}")
