import os

from kubernetes import config

from testing.kubectl import create_dai_license
from testing.kubectl import kubectl_apply
from testing.kubectl import kubectl_delete_resource_all
from testing.kubectl import setup_mlops_secrets

config.load_config()
system_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")

kubectl_delete_resource_all(resource="daiv", namespace=system_namespace)
kubectl_apply(
    path=(os.path.join(os.path.dirname(__file__), "test_data", "dai_versions")),
    namespace=system_namespace,
)
kubectl_delete_resource_all(resource="h2ov", namespace=system_namespace)
kubectl_apply(
    path=(os.path.join(os.path.dirname(__file__), "test_data", "h2o_versions")),
    namespace=system_namespace,
)
kubectl_delete_resource_all(resource="daistp", namespace=system_namespace)
kubectl_apply(
    path=(os.path.join(os.path.dirname(__file__), "test_data", "dai_setups")),
    namespace=system_namespace,
)
kubectl_delete_resource_all(resource="h2ostp", namespace=system_namespace)
kubectl_apply(
    path=(os.path.join(os.path.dirname(__file__), "test_data", "h2o_setups")),
    namespace=system_namespace,
)

create_dai_license(namespace=system_namespace)

if os.getenv("MLOPS_CLUSTER") == "true":
    setup_mlops_secrets(namespace=system_namespace)
