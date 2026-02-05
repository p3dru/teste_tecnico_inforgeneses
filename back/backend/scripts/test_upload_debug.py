import requests
import sys

BASE_URL = "http://localhost:8000"

def run():
    # 1. Signup/Login
    username = "debug_user_1"
    password = "password123"
    
    print(f"[-] Registering user {username}...")
    requests.post(f"{BASE_URL}/auth/users", json={"username": username, "password": password})
    
    print(f"[-] Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/token", data={"username": username, "password": password})
    if resp.status_code != 200:
        print(f"[!] Login failed: {resp.text}")
        return
        
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[+] Logged in. Token partial: {token[:10]}...")

    # 2. Upload
    print(f"[-] Attempting Upload...")
    
    # Create dummy file content
    files = {
        'file': ('test_image.jpg', b'fake_image_content', 'image/jpeg')
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/files/upload", headers=headers, files=files)
        print(f"[*] Response Status: {resp.status_code}")
        print(f"[*] Response Body: {resp.text}")
    except Exception as e:
        print(f"[!] Request Exception: {e}")

if __name__ == "__main__":
    run()
