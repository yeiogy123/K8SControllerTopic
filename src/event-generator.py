import time
import requests
from kubernetes import client, config
import os

config.load_incluster_config()  # Load the in-cluster Kubernetes configuration
v1 = client.CoreV1Api()

def send_request_and_generate_event():
    namespace = "default"
    event_name = "custom_event"

    hub = os.environ.get('SELENIUM_HUB_SERVICE_HOST')
    number_running = None

    while True:
        try:
            pods = v1.list_namespaced_pod(namespace, label_selector="job-name=selenium-node-chrome", field_selector="status.phase=Running")
            number_running = len(pods.items)
            print("Number of running pods: ", str(number_running))

            response = requests.get('http://' + hub + ':4444/se/grid/newsessionqueue/queue', timeout=5)
            response.raise_for_status()
            value = len(response.json()['value'])
            print("Number of sessions: ", str(value))

            if value != number_running:
                event = {
                    "apiVersion": "v1",
                    "kind": "Event",
                    "metadata": {
                        "name": event_name,
                        "labels": {
                            "SessionCount": str(value)
                        }
                    }
                }
                
                try:
                    events = v1.list_namespaced_event(namespace=namespace, label_selector="SessionCount")
                    if events.items:
                        print(f"Custom event already existing")
                        v1.delete_namespaced_event(name=event_name, namespace=namespace)
                    v1.create_namespaced_event(namespace=namespace, body=event)
                    print(f"Created new event custom-event with SessionCount: {value}")
                except client.exceptions.ApiException as e:
                    print(f"Failed to create or update event custom-event: {e}")

        except requests.exceptions.RequestException as e:
            print("Error occurred during the request:", str(e))

        time.sleep(2)

if __name__ == '__main__':
    send_request_and_generate_event()
