from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import sys

def shutdown_vm(subscription_id: str, resource_group: str, vm_name: str):
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    # Get VM instance view to check power state
    instance_view = compute_client.virtual_machines.instance_view(resource_group, vm_name)
    statuses = instance_view.statuses
    power_state = next((s.display_status for s in statuses if s.code.startswith('PowerState')), None)

    print(f"VM '{vm_name}' in resource group '{resource_group}' is currently: {power_state}")

    if power_state == "VM running":
        print("Shutting down VM...")
        async_shutdown = compute_client.virtual_machines.begin_power_off(resource_group, vm_name)
        async_shutdown.wait()
        print(f"VM '{vm_name}' has been shut down.")
    else:
        print(f"VM '{vm_name}' is not running. No action taken.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python shutdown_vm.py <subscription_id> <resource_group> <vm_name>")
        sys.exit(1)