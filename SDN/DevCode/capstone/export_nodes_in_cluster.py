from kubernetes import client, config

def export_all_pods():
    # Cấu hình client Kubernetes
    config.load_kube_config()

    # Tạo đối tượng Kubernetes API client
    v1 = client.CoreV1Api()

    # Liệt kê tất cả các Pods
    pods = v1.list_pod_for_all_namespace(watch=False)

    # Xuất thông tin của các Pods
    for pod in pods.items:
        print(f"Namespace: {pod.metadata.namespace}, Name: {pod.    metadata.name}, Status: {pod.status.phase}")

if __name__ == "__main__":
    export_all_pods()
