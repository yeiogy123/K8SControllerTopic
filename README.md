## To deploy and monitor selenium grid on minikube
```bash

$ minikube dashboard
# Open the URL and monitor the cluster

$ kubectl create -f node-chrome-job.yaml

$ kubectl create -f role.yaml

$ kubectl create -f hub-deployment.yaml

$ minikube service selenium-hub --url
# Open the last URL and copy it to `testcase.py` under the `command_executor` section.

$ kubectl create -f controller.yaml

$ python testcase.py
# Execute the testcase
$ ./script.sh 10
# Ensure that the shell script is executable. Specify the number of test cases you wish to execute, for example, "5"

```

### To test the images with docker compose
```bash
$ docker compose up

# docker compose down
```

### Please note that these images are intended for arm64 architecture only.
