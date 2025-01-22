from .utils import (
    delete_efs_csi_driver,
    delete_aws_nginx_controller,
    unconfigure_current_kubeconfig,
    destroy_terraform,
)

from cloudkube.ClusterManager import ClusterManager


if __name__ == "__main__":
    cfg = ClusterManager.__parse_config()
    if not cfg:
        print(
            "Invalid configuration file provided. Have you run '2. Configure cluster configuration?'"
        )
        exit(1)
    # User Prompt
    confirm = input(
        "Before tearing down the infrastructure, it is good practice to have removed all your kubernetes pods, services, and everything that was created using the kubernetes manifest. This is so as to ensure no dangling services on the cloud, such load balancers, which could cause infrastructure deprovisioning to fail. To confirm proceed, (y/N): "
    )

    if confirm == "y":

        # Clean up procedure
        # Order is important here, we are deleting in the reverse order that we created
        # create A -> create B -> create C -> destroy C -> destroy B -> destroy A
        # delete_efs_csi_driver("kubernetes-sigs/aws-efs-csi-driver", ref="release-2.0")
        if cfg["require_efs"]:
            delete_efs_csi_driver(
                "kubernetes-sigs/aws-efs-csi-driver", ref="release-2.0"
            )
        if cfg["ingress_controller"] != "None":
            delete_aws_nginx_controller(cfg["ingress_controller"])
        unconfigure_current_kubeconfig()
        destroy_terraform()
        exit(0)
    else:
        exit(1)
