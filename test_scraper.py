from providers.cricket import CricketProvider
import time

print("Testing CricketProvider...")
provider = CricketProvider()
try:
    matches = provider.get_matches()
    print(f"Found {len(matches)} matches.")
    for m in matches:
        print(m)
except Exception as e:
    print(f"CRASH: {e}")
    import traceback
    traceback.print_exc()
