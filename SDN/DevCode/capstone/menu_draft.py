import kubernetes
from kubernetes import client, config
from kubernetes.config.kube_config import yaml
import os
import subprocess
import json


def execute_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")

def display_namespace():
     #Lấy danh sách các Namespace từ Kubernetes Cluster
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


def display_pods(namespace):
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

def display_network_policy_menu():
    print("Menu Network Policy:")
    print("1. Deny_all_traffic_to_an_application.")
    print("2. Limit_traffic_to_an_application")
    print("3. Deny_all_none_whitelisted_traffic_to_a_name_space")
    print("4. Deny_all_traffic_from_other_namespace")

def main_menu():
    selected_namespace = ""
    while True:
        print("Main Menu:")
        print("1. Hiển thị danh sách Namespace và chọn Namespace")
        print("2. Chọn Pod trong Namespace")
        print("3. Thoát")

        choice = input("Chọn tùy chọn: ")
        
        if choice == "1":
            namespaces = display_namespace()
            selected_namespace = select_namespace(namespaces)
            # with open("namespace.json", "w") as config_file:
            #     config = {"namespace": selected_namespace , "pod" : None}
            #     json.dump(config, config_file)
                
        elif choice == "2":
            if selected_namespace is None:
                print("Bạn cần chọn Namespace trước.")
            else:
                pods = display_pods(selected_namespace)
                selected_pods = select_pod(pods)
                with open("namespace.json", "w") as config_file:
                    config = {"namespace": selected_namespace , "pod" : selected_pods}
                    json.dump(config, config_file)
                display_network_policy_menu()
                pod_choice = input("Chọn tùy chọn cho Pod: ")
                handle_policy_choice(pod_choice)
        elif choice == "3":
            break
        else:
            print("Tùy chọn không hợp lệ.")


def handle_policy_choice(choice):
    if choice == "1":
        execute_script("01_Deny_all_traffic_to_an_application.py")
    elif choice == "2":
        execute_script("02_Limit_traffic_to_an_application.py")
    elif choice == "3":
        execute_script("03_Deny_all_none_whitelisted_traffic_to_a_name_space.py")
    elif choice == "4":
        execute_script("04_Deny_all_traffic_from_other_namespace.py")
    else:
        print("Tùy chọn không hợp lệ cho Pod.")

config.load_kube_config()

if __name__ == "__main__":
    main_menu()
    
