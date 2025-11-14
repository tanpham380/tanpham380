# SDN - Project

This folder contains the SDN (Software Defined Networking) project by Pham Thanh Tan. Objective: Research and implement network policies (NetworkPolicy), HA (Keepalived/HAProxy), deployment on Kubernetes, testing, and reporting.

## Overview Structure

- `configure/` - Configuration files and notes (Keepalived, HA configs, DNS hosts, Kubernetes show outputs, YAML samples).
- `DevCode/` - Source code for the project, including Python scripts, network policy examples, and the `capstone/` folder with main tasks.
  - `DevCode/capstone/` - Set of scripts: `01_*`..`04_*` (network policy exercises), `import-kubernetes.py`, `export_nodes_in_cluster.py`, `policy-blockping.yaml`...
- `test/` - Test scripts (e.g., `test.py`, `viewpod.py`, `network_policy.yaml`).
- `Flowchart/`, `Image/`, `Report/`, `Slide/`, `video/` - Project artifacts: flowcharts, images, slides, reports, demo videos.

## Project Objectives

- Design and apply NetworkPolicy for applications on Kubernetes (deny-by-default, whitelist services, limit traffic between namespaces).
- Deploy HA for services (Keepalived / HAProxy configs included).
- Write scripts to automate cluster configuration import/export, policy testing, and log collection.

## Prerequisites

- Kubernetes cluster (minikube / kind / k8s cluster). Scripts assume `kubectl` is configured.
- Python 3.x (if running `DevCode/*.py`).
- Access to apply YAML (`kubectl apply`) and view Pods/Namespaces.

## Quick Start

1. Check configuration contents:

   ```bash
   ls -la SDN/configure
   ```

2. Read sample policies:

   ```bash
   cat SDN/DevCode/capstone/policy-blockping.yaml
   ```

3. Apply a test policy (e.g., `policy-blockping.yaml`):

   ```bash
   kubectl apply -f SDN/DevCode/capstone/policy-blockping.yaml
   ```

4. Run import/export scripts (example):

   ```bash
   python3 SDN/DevCode/capstone/import-kubernetes.py
   ```

5. Run viewpod test:

   ```bash
   python3 SDN/test/viewpod.py
   ```

## Important Files

- `SDN/configure/Keepalived.txt` - Keepalived notes/config.
- `SDN/configure/haconfig.txt` - HA configuration.
- `SDN/DevCode/capstone/01_Deny_all_traffic_to_an_application.py` - Deny all example.
- `SDN/DevCode/capstone/02_Limit_traffic_to_an_application.py` - Limited traffic example.
- `SDN/DevCode/capstone/policy-blockping.yaml` - Policy to block ICMP ping.

## Testing and Verification

- After applying NetworkPolicy, use `kubectl exec` or `kubectl run` to check connectivity between Pods.
- View logs and events: `kubectl describe pod <pod>` and `kubectl logs <pod>`.

## Next Steps

- Add CI workflow to automatically run tests (e.g., `kubectl apply` on kind/minikube in GitHub Actions).
- Add Helm chart examples for deployment and policy templates.
- Automate report collection (run `export_nodes_in_cluster.py` periodically).

## Contact

For help running or expanding the project, email: Phamthanhtanlop92@gmail.com
