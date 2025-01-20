import os

from kubernetes import config

from testing.kubectl import create_dai_license
from testing.kubectl import kubectl_apply
from testing.kubectl import kubectl_delete_resource_all

config.load_config()
system_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")

kubectl_delete_resource_all(resource="daiv", namespace=system_namespace)
kubectl_apply(
    path=(os.path.join(os.path.dirname(__file__), "test_data_full", "dai_versions")),
    namespace=system_namespace,
)
kubectl_delete_resource_all(resource="daistp", namespace=system_namespace)
kubectl_apply(
    path=(os.path.join(os.path.dirname(__file__), "test_data_full", "dai_setups")),
    namespace=system_namespace,
)

create_dai_license(namespace=system_namespace)
