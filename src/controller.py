from kubernetes import client, config, watch


config.load_incluster_config()  # Load the in-cluster Kubernetes configuration
v1 = client.BatchV1Api()

def event_handler(event):
    job_name = "selenium-node-chrome"
    namespace = event['object'].metadata.namespace
    if event['object'].metadata.labels:
        session_count = event['object'].metadata.labels.get('SessionCount')
        print("Session Count is : " + session_count)

        try:
            job = v1.read_namespaced_job(name=job_name, namespace=namespace)
            job.spec.parallelism = int(session_count)
            v1.patch_namespaced_job(name=job_name, namespace=namespace, body=job)
            print(f"Modified Job {job_name} parallelism to {session_count}")
        except Exception as e:
            print(f"Error modifying Job {job_name}: {str(e)}")

def watch_events():
    v1_event = client.CoreV1Api()
    w = watch.Watch()

    for event in w.stream(v1_event.list_event_for_all_namespaces):
        if event['object'].metadata.name == 'custom_event':
            print("Custom event found.")
            event_handler(event)

if __name__ == '__main__':
    watch_events()