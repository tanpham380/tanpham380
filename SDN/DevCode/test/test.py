import yaml

raw_data = {
    'api_version': 'networking.k8s.io/v1',
    'kind': 'NetworkPolicy',
    'metadata': {
        'annotations': {
            'kubectl.kubernetes.io/last-applied-configuration': '{"apiVersion":"networking.k8s.io/v1","kind":"NetworkPolicy","metadata":{"annotations":{},"name":"deny-appa-to-appb","namespace":"tools"},"spec":{"ingress":[{"from":[{"podSelector":{"matchExpressions":[{"key":"app","operator":"NotIn","values":["AppA"]}]}}]}],"podSelector":{"matchLabels":{"app":"AppB"}},"policyTypes":["Ingress"]}}\n'
        },
        'creation_timestamp': '2023-10-31T08:33:38Z',
        'deletion_grace_period_seconds': None,
        'deletion_timestamp': None,
        'finalizers': None,
        'generate_name': None,
        'generation': 1,
        'labels': None,
        'managed_fields': [
            {
                'api_version': 'networking.k8s.io/v1',
                'fields_type': 'FieldsV1',
                'fields_v1': {
                    'f:metadata': {
                        'f:annotations': {
                            '.': {},
                            'f:kubectl.kubernetes.io/last-applied-configuration': {}
                        }
                    },
                    'f:spec': {
                        'f:ingress': {},
                        'f:podSelector': {},
                        'f:policyTypes': {}
                    }
                },
                'manager': 'kubectl-client-side-apply',
                'operation': 'Update',
                'subresource': None,
                'time': '2023-10-31T08:33:38Z'
            }
        ],
        'name': 'deny-appa-to-appb',
        'namespace': 'tools',
        'owner_references': None,
        'resource_version': '11468110',
        'self_link': None,
        'uid': 'af39be0c-5f8c-4438-9afe-99a37a8e9d2c'
    },
    'spec': {
        'egress': None,
        'ingress': [
            {
                '_from': [
                    {
                        'ip_block': None,
                        'namespace_selector': None,
                        'pod_selector': {
                            'match_expressions': [
                                {
                                    'key': 'app',
                                    'operator': 'NotIn',
                                    'values': ['AppA']
                                }
                            ],
                            'match_labels': None
                        }
                    }
                ],
                'ports': None
            }
        ],
        'pod_selector': {
            'match_expressions': None,
            'match_labels': {
                'app': 'AppB'
            }
        },
        'policy_types': ['Ingress']
    }
}

formatted_yaml = yaml.dump({
    'apiVersion': raw_data['api_version'],
    'kind': raw_data['kind'],
    'metadata': {
        'name': raw_data['metadata']['name'],
        'namespace': raw_data['metadata']['namespace']
    },
    'spec': {
        'podSelector': raw_data['spec']['pod_selector'],
        'policyTypes': raw_data['spec']['policy_types'],
        'ingress': raw_data['spec']['ingress']
    }
}, default_flow_style=False)

print(formatted_yaml)
