import requests
import os
import yaml

KESTRA_URL = "http://localhost:8080/api/v1/flows"
AUTH = ("admin@kestra.io", "Admin1234")

FLOWS_DIR = "../../kestra/flows"

def register_flow(file_path):
    with open(file_path, 'r') as f:
        flow_content = f.read()
        
    # Kestra API expects the YAML content in the body
    headers = {"Content-Type": "application/x-yaml"}
    
    print(f"Registering {file_path}...")
    try:
        response = requests.post(
            KESTRA_URL, 
            data=flow_content,
            headers=headers,
            auth=AUTH
        )
        if response.status_code == 200:
            print(f"✅ Success: {response.json().get('id')}")
        else:
            print(f"❌ Failed ({response.status_code}): {response.text}")
    except Exception as e:
         print(f"❌ Connection Error: {str(e)}")

if __name__ == "__main__":
    # Walk through kestra/flows directory
    base_path = os.path.join(os.path.dirname(__file__), FLOWS_DIR)
    
    if not os.path.exists(base_path):
        print(f"Directory not found: {base_path}")
        exit(1)
        
    for filename in os.listdir(base_path):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            register_flow(os.path.join(base_path, filename))
