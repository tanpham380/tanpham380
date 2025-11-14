from kubernetes import client, config
import yaml

def create_network_policy(namespace, policy_name, policy_yaml):
    config.load_kube_config()  # Hoặc sử dụng config.load_incluster_config() nếu bạn đang chạy trong một pod

    v1 = client.NetworkingV1Api()
    
    body = client.NetworkingV1NetworkPolicy(
        api_version="networking.k8s.io/v1",
        kind="NetworkPolicy",
        metadata=client.V1ObjectMeta(name=policy_name),
        spec=policy_yaml
    )

    try:
        response = v1.create_namespaced_network_policy(namespace, body)
        print(f"Network Policy '{policy_name}' created successfully.")
        return response
    except Exception as e:
        print(f"Error creating Network Policy: {e}")
        return None

def get_network_policy(name , namespace):
    config.load_kube_config()
    v1 = client.NetworkingV1Api()

    try:
        namespace = namespace
        policy_name = name

        policy = v1.read_namespaced_network_policy(name=policy_name, namespace=namespace)
        print(f"Network Policy '{policy_name}':\n{policy}")
        return policy
    except Exception as e:
        print(f"Error getting Network Policy: {e}")
        return None


def delete_network_policy(namespace, policy_name):
    config.load_kube_config()
    v1 = client.NetworkingV1Api()

    try:
        response = v1.delete_namespaced_network_policy(name=policy_name, namespace=namespace)
        print(f"Network Policy '{policy_name}' deleted successfully.")
        return response
    except Exception as e:
        print(f"Error deleting Network Policy: {e}")
        return None


def export_network_policy(namespace, policy_name, file_path):
    config.load_kube_config()
    v1 = client.NetworkingV1Api()

    try:
        policy = v1.read_namespaced_network_policy(
            name=policy_name, namespace=namespace)
        print(policy)

        formatted_policy = {
            'apiVersion': policy.api_version,
            'kind': policy.kind,
            'metadata': {
                'name': policy.metadata.name,
                'namespace': policy.metadata.namespace
            },
            'spec': {
                'podSelector': policy.spec.pod_selector.to_dict(),
                'policyTypes': policy.spec.policy_types,
                'ingress': [ingress.to_dict() for ingress in policy.spec.ingress]
            }
        }

        with open(file_path, 'w') as outfile:
            yaml.dump(formatted_policy, outfile, default_flow_style=False)

        print(f"Network Policy '{policy_name}' exported to '{file_path}'.")
        return True
    except Exception as e:
        print(f"Error exporting Network Policy: {e}")
        return False


if __name__ == "__main__":
    namespace = "tools"
    policy_name = "deny-appa-to-appb"
    policy_yaml = {
        # Định nghĩa chính sách tại đây (dưới dạng Python dictionary)
    }

    # create_network_policy(namespace, policy_name, policy_yaml)
    # get_network_policy(policy_name,namespace)
    export_network_policy(namespace, policy_name, 'network_policy.yaml')
    # fix_exported_policy('network_policy.yaml')
    # delete_network_policy(namespace, policy_name)
