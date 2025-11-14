import yaml
import subprocess
import kubernetes
import json

# namespace = selected_namespace
with open("namespace.json", "r") as config_file:
    config = json.load(config_file)
pod_name = config["node"]

network_policy = {
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

def apply_kubernetes_yaml(yaml_file_path):
    try:
        # The command you would normally type in the terminal
        cmd = ['kubectl', 'apply', '-f', yaml_file_path]
        
        # Execute the command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Print the output from the command
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        # If the command failed, it will raise this exception
        print("Error applying YAML:", e.stderr)
    except Exception as e:
        # Catch-all for any other exceptions
        print("An error occurred:", str(e))

while True:
            # Menu
        print("1. Thực thi")
        print("2. Xuất ra file yaml với tên do bạn chọn")
        choice = input("Chọn một lựa chọn (1 hoặc 2): ")

        if choice == "1":
            Limit_traffic_to_an_application_yaml = yaml.dump(network_policy, default_flow_style=False)
            with open("Limit_traffic_to_an_application_yaml", "w") as temp_file:
                temp_file.write(Limit_traffic_to_an_application_yaml)
            apply_kubernetes_yaml('Limit_traffic_to_an_application_yaml')

            break
        elif choice == "2":
            filename = input("Nhập tên file bạn muốn lưu (ví dụ: data.yaml): ")
            with open(filename, 'w') as file:
                yaml.dump(network_policy, file)
            print(f"Đã lưu vào {filename}.yaml!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            