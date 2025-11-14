from kubernetes import client, config

# Load kubeconfig file (you can skip this if running in a Kubernetes cluster)
config.load_kube_config()

# Create a Kubernetes client
api_instance = client.CoreV1Api()

# Specify the namespace you're interested in
namespace = "your_namespace"

# Get all pods in the specified namespace
pods = api_instance.list_namespaced_pod(namespace)

# Iterate through the pods and print their labels
for pod in pods.items:
    pod_name = pod.metadata.name
    pod_labels = pod.metadata.labels
    print(f"Pod: {pod_name}, Labels: {pod_labels}")
