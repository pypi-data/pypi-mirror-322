import requests
import json
import time


def run_protocol(robot_ip, protocol_file):
    base_url = f"http://{robot_ip}:31950"
    headers = {"Opentrons-Version": "3", "Content-Type": "application/json"}

    def check_robot_status():
        """Check the robot's status before proceeding."""
        url = f"{base_url}/health"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get("status") == "ok":
                    print("Robot is available and ready.")
                    return True
                else:
                    print(f"Robot status is not OK: {health_data}")
            else:
                print(f"Failed to fetch robot status: {response.json()}")
        except Exception as e:
            print(f"Error checking robot status: {e}")
        return False

    def upload_protocol():
        """Upload a protocol to the robot."""
        url = f"{base_url}/protocols"
        files = {"files": open(protocol_file, "rb")}
        response = requests.post(url, headers={"Opentrons-Version": "3"}, files=files)
        response_data = response.json()

        if "data" in response_data and "id" in response_data["data"]:
            protocol_id = response_data["data"]["id"]
            print(f"Protocol uploaded successfully. Protocol ID: {protocol_id}")
            return protocol_id
        else:
            print(f"Failed to upload protocol: {response_data}")
            return None

    def create_run(protocol_id):
        """Create a run using the uploaded protocol."""
        url = f"{base_url}/runs"
        data = {"data": {"protocolId": protocol_id}}
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        if response.status_code == 201:
            run_id = response_data["data"]["id"]
            print(f"Run created successfully. Run ID: {run_id}")
            return run_id
        else:
            print(f"Failed to create run: {response_data}")
            return None

    def start_run(run_id):
        """Start the run."""
        url = f"{base_url}/runs/{run_id}/actions"
        data = {"data": {"actionType": "play"}}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print("Run started successfully.")
        else:
            print(f"Failed to start run: {response.json()}")

    def monitor_run_status(run_id):
        """Wait for the run to complete."""
        url = f"{base_url}/runs/{run_id}"
        while True:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                run_data = response.json()
                status = run_data["data"]["status"]
                print(f"Current run status: {status}")
                if status in ["succeeded", "failed", "stopped"]:
                    print(f"Run finished with status: {status}")
                    break
                time.sleep(5)  # Wait before polling again
            else:
                print(f"Failed to monitor run: {response.json()}")
                break

    # # Step 1: Check robot status
    # if not check_robot_status():
    #     print("Robot is not available. Exiting.")
    #     return

    # Step 2: Upload the protocol
    protocol_id = upload_protocol()
    if not protocol_id:
        return

    # Step 3: Create a run
    run_id = create_run(protocol_id)
    if not run_id:
        return

    # Step 4: Start the run
    start_run(run_id)

    # Step 5: Wait for the run to complete
    monitor_run_status(run_id)