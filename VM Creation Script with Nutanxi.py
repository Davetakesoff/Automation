import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json

# Suppress SSL warnings (self-signed cert)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Config
PRISM_IP = "<your-prism-ip>"
USERNAME = "<your-username>"
PASSWORD = "<your-password>"
BASE_URL = f"https://{PRISM_IP}:9440/api/nutanix/v2.0"
AUTH = HTTPBasicAuth(USERNAME, PASSWORD)

# ── CREATE VM ──────────────────────────────────────────────
def create_vm(name):
    payload = {
        "name": name,
        "memory_mb": 1024,
        "num_vcpus": 1,
        "num_cores_per_vcpu": 1
    }

    response = requests.post(
        f"{BASE_URL}/vms",
        json=payload,
        auth=AUTH,
        verify=False
    )

    if response.status_code == 201:
        vm_uuid = response.json()["task_uuid"]  # Nutanix returns a task, not UUID directly
        print(f"VM creation task triggered: {vm_uuid}")
        return response.json()
    else:
        print(f"Failed: {response.status_code} — {response.text}")

# ── DELETE VM ──────────────────────────────────────────────
def delete_vm(vm_uuid):
    response = requests.delete(
        f"{BASE_URL}/vms/{vm_uuid}",
        auth=AUTH,
        verify=False
    )

    if response.status_code == 201:
        print(f"VM deletion task triggered for {vm_uuid}")
    else:
        print(f"Failed: {response.status_code} — {response.text}")

# ── RUN ────────────────────────────────────────────────────
create_vm("test-vm-01")