import requests
import time

BASE_URL = "http://localhost:8001"

print("="*60)
print("End-to-End Test - Testing http://localhost:8001")
print("="*60)

# Test 1: Create session
print("\n[1/2] Creating session...")
try:
    r = requests.post(f"{BASE_URL}/api/session/create", timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
    
    if r.status_code == 200:
        session_id = r.json()["data"]["session_id"]
        print(f"Session created: {session_id}")
        
        # Test 2: Send message
        print("\n[2/2] Sending message...")
        data = {"session_id": session_id, "message": "推荐一款手机"}
        r = requests.post(f"{BASE_URL}/api/chat/send", json=data, timeout=30)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            result = r.json()["data"]
            print(f"\n✅ SUCCESS!")
            print(f"Reply: {result['reply']}")
            print(f"Intent: {result['intent']['name']} (confidence: {result['intent']['confidence']})")
        else:
            print(f"❌ Failed with status: {r.status_code}")
            print(f"Response: {r.text}")
    else:
        print("❌ Failed to create session")
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error! Is the backend running on port 8001?")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
