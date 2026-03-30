import requests
import json
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
PRISM_IP = "your_nutanix_ip"
USERNAME = "your_username"
PASSWORD = "your_password"
VM_UUID = "your_vm_uuid"

# Function for snapshot creation. Contains a function, dictionary parameters and response
def create_snapshot(vm_uuid, snapshot_name):
    url = f"https://{PRISM_IP}:9440/api/nutanix/v2.0/snapshots"
# Dictionary parameters
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "snapshot_specs": [
            {
                "vm_uuid": vm_uuid,
                "snapshot_name": snapshot_name
            }
        ]
    }
# Response
    response = requests.post(
        url,
        headers=headers,
        auth=(USERNAME, PASSWORD),
        json=payload,
        verify=False
    )

    return response


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"auto_snapshot_{timestamp}"

    response = create_snapshot(VM_UUID, snapshot_name)

    if response.status_code == 200:
        print(f"Snapshot created: {snapshot_name}")
    else:
        print(f"Failed: {response.status_code}")


main()