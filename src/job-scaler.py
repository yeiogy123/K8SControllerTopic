import time
import requests
from kubernetes import client, config
import os

def scale_jobs(job_name, replica_count):
    config.load_incluster_config()  # Load the in-cluster Kubernetes configuration
    api_instance = client.BatchV1Api()

    job = api_instance.read_namespaced_job(name=job_name, namespace='default')
    job.spec.parallelism = replica_count

    api_instance.patch_namespaced_job(name=job_name, namespace='default', body=job)

def fetch_pod_info():
    hub = os.environ.get('SELENIUM_HUB_SERVICE_HOST')
    previous_value = 0
    while True:
        try:
            response = requests.get('http://' + hub + ':4444/se/grid/newsessionqueue/queue', timeout=5)
            response.raise_for_status()  # Raise an exception if the response status code is an error
        
            value = response.json()['value']
            replica_count = len(value)
            if replica_count != previous_value:
                print("Number of sessions: ", replica_count)
                scale_jobs(job_name='selenium-node-chrome', replica_count=replica_count)
                previous_value = replica_count

        except requests.exceptions.RequestException as e:
            print("Error occurred during the request:", str(e))

        time.sleep(3)

if __name__ == '__main__':
    fetch_pod_info()

