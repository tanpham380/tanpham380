import kubernetes
from kubernetes import client, config
from kubernetes.config.kube_config import yaml


def get_namespaces():
    # Lấy danh sách các Namespace từ Kubernetes Cluster
    namespaces = []
    for ns in client.CoreV1Api().list_namespace().items:
        namespaces.append(ns.metadata.name)
    return namespaces

def select_namespace(namespaces):
    # Hiển thị danh sách Namespace và cho phép chọn
    print("Danh sách Namespace:")
    for i, ns in enumerate(namespaces):
        print(f"{i + 1}. {ns}")
    selected = input("Chọn Namespace (nhập số tương ứng): ")
    return namespaces[int(selected) - 1]

def get_pods_in_namespace(namespace):
    # Lấy danh sách các Pod trong Namespace
    pods = []
    for pod in client.CoreV1Api().list_namespaced_pod(namespace).items:
        pods.append(pod.metadata.name)
    return pods

def select_pod(pods):
    # Hiển thị danh sách Pod và cho phép chọn
    print("Danh sách Pod:")
    for i, pod in enumerate(pods):
        print(f"{i + 1}. {pod}")
    selected = input("Chọn Pod (nhập số tương ứng): ")
    return pods[int(selected) - 1]

def list_network_policies(namespace):
    # Lấy danh sách các Network Policy trong Namespace
    policies = client.NetworkingV1Api().list_namespaced_network_policy(namespace)
    print("Danh sách Network Policy:")
    for policy in policies.items:
        print(policy.metadata.name)


def deny_all(namespace, pod_name):
    existing_policies = client.NetworkingV1Api().list_namespaced_network_policy(namespace)
    for existing_policy in existing_policies.items:
        if existing_policy.metadata.name == f"{pod_name}-deny-policy":
            print(f"Network Policy cho Pod {pod_name} đã tồn tại.")
            return 
    policy_deny = {
        "kind": "NetworkPolicy",
        "apiVersion": "networking.k8s.io/v1",
        "metadata": {
            "name": f"{pod_name}-deny-policy"  
        },
        "spec": {
            "podSelector": {
                "matchLabels": {
                    "app": pod_name  
                }
            },
            "ingress": []
        }
    }
    return policy_deny

def allow_policy(namespace, pod_name):
    existing_policies = client.NetworkingV1Api().list_namespaced_network_policy(namespace)
    for existing_policy in existing_policies.items:
        if existing_policy.metadata.name == f"{pod_name}-allow-policy":
            print(f"Network Policy cho Pod {pod_name} đã tồn tại.")
            return  
    policy_allow = {
        "kind": "NetworkPolicy",
        "apiVersion": "networking.k8s.io/v1",
        "metadata": {
            "name": f"{pod_name}-allow-policy" 
        },
        "spec": {
            "podSelector": {
                "matchLabels": {
                    "app": pod_name  
                }
            },
            "ingress": []
        }
    }
    return policy_allow

def export_network_policy (namespace, policy_name, file_path):
    config. load_kube_config()
    v1 = client.NetworkingV1Api()
    try:
        policy = v1. read_namespaced_network_policy (name=policy_name, namespace=namespace)
        with open(file_path, 'w') as outfile:
            yaml.dump((policy.to_dict), outfile, default_flow_style=False) 
            print (f"Network Policy '{policy_name}' exported to '{file_path}'.")
        return True
    except Exception as e:
        print(f"Error exporting Network Policy: {e}")
        return False

'''def confirm_apply(namespace, pod_name, policy):
    confirm = input ("Xác nhận áp dụng policy: "Y" để áp dụng, "N" để trở về ")
    if confirm.lower == "y":
        client.NetworkingV1Api().create_namespaced_network_policy(namespace, policy)
        print(f"Network Policy đã được áp dụng cho Pod {pod_name} thành công!")
    elif confirm.lower == "n":
        print(f"Không áp dụng policy")'''

'''def apply_network_policy(namespace, pod_name):
    # Điều chỉnh Network Policy cho Pod trong Namespace
    policy = {
        "kind": "NetworkPolicy",
        "apiVersion": "networking.k8s.io/v1",
        "metadata": {
            "name": "example-policy"
        },
        "spec": {
            "podSelector": {
                "matchLabels": {
                    "app": pod_name  # Sử dụng tên Pod cho nhãn app
                }
            },
            "ingress": []
        }
    }

    # Áp dụng Network Policy
    client.NetworkingV1Api().create_namespaced_network_policy(namespace, policy)
    print(f"Network Policy đã được áp dụng cho Pod {pod_name} thành công!")

   '''

if __name__ == "__main__":
    config.load_kube_config()  # Load cấu hình Kubernetes từ môi trường

    while True:
        print("\nMenu:")
        print("1. Hiển thị danh sách Namespace và chọn")
        print("2. Chọn Pod trong Namespace")
        print("3. Hiển thị danh sách Network Policy và Apply Network Policy")
        print("4. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == "1":
            namespaces = get_namespaces()
            selected_namespace = select_namespace(namespaces)
        elif choice == "2":
            pods = get_pods_in_namespace(selected_namespace)
            selected_pod = select_pod(pods)
        elif choice == "3":
            print("1. Allow all")
            print("2. Deny all")
            choose = input("Chon policy muon apply")
            if choose == "1":
                allow_policy(selected_namespace, selected_pod)
                selected_policy = allow_policy(selected_namespace, selected_pod)
            elif choose == "2":
                deny_all(selected_namespace, selected_pod)
                selected_policy = deny_all(selected_policy, selected_pod)
            confirm = input (" Xác nhận áp dụng policy: Y để áp dụng, N để trở về ")
            if confirm.lower == "y":
                client.NetworkingV1Api().create_namespaced_network_policy(selected_namespace,selected_policy)
                print(f"Network Policy đã được áp dụng cho Pod {selected_pod} thành công!")
            elif confirm.lower == "n":
                    print(f"Không áp dụng policy")

            choose2 = input("Ban co muon xuat file hay khong? Y/N")
            if choose2.lower == "y":
                file_path = input("Chon file path de luu")
                export_network_policy(selected_namespace, selected_pod, file_path)
            elif choose2.lower == "n":
                break
        elif choice == "4":
            print("Thanks for using this product!!!\n")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")