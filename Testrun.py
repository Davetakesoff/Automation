import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PRISM_IP = ""
USERNAME = ""
PASSWORD = ""
BASE_URL = f"https://{PRISM_IP}:9440/api/nutanix/v2.0"
AUTH = HTTPBasicAuth(USERNAME, PASSWORD)


def get_user_input():
    print("\n── VM Provisioning Tool ──\n")

    name = input("VM Name: ")

    memory_gb = int(input("Memory (GB): "))
    memory_mb = memory_gb * 1024

    cpu = int(input("CPU cores: "))

    disk_gb = int(input("Disk size (GB): "))

    return {
        "name": name,
        "memory_mb": memory_mb,
        "num_vcpus": cpu,
        "disk_size": disk_gb * 1024 * 1024 * 1024
    }

def create_vm(spec):

    payload = {
        "name": spec["name"],
        "memory_mb": spec["memory_mb"],
        "num_vcpus": spec["num_vcpus"],
        "num_cores_per_vcpu": 1,

        # ── DISK (required) ───────────────────────────────
        "vm_disks": [
            {
                "disk_address": {
                    "device_bus": "SCSI",
                    "device_index": 0
                },
                "vm_disk_create": {
                    "storage_container_uuid": "",
                    "size": spec["disk_size"]
                }
            }
        ],

        # ── NETWORK (required) ─────────────────────────────
        "vm_nics": [
            {
                "network_uuid": ""
            }
        ]
    }

    response = requests.post(
        f"{BASE_URL}/vms",
        json=payload,
        auth=AUTH,
        verify=False
    )

    if response.status_code == 201:
        vm_uuid = response.json()["task_uuid"]
        print(f"VM creation task triggered: {vm_uuid}")
        return response.json()
    else:
        print(f"Failed: {response.status_code} — {response.text}")

specs = get_user_input()
create_vm(specs)
