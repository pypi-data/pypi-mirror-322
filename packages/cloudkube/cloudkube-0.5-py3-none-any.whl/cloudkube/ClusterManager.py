from .utils import (
    apply_terraform,
    configure_kubectl,
    install_ingress_controller,
    apply_efs_csi_driver,
    delete_aws_nginx_controller,
    delete_efs_csi_driver,
    unconfigure_current_kubeconfig,
    destroy_terraform,
    clean_local_config_json,
)
import json


class ClusterManager:
    @staticmethod
    def __parse_config(path_to_config):
        try:
            res = None
            with open(path_to_config, "r") as f:
                res = json.load(f)

            region = res["region"]
            prefix = res["prefix"]
            architecture = res["architecture"]
            ingress_controller = res["ingressController"]
            require_efs = bool(res["requireEFS"])

        except:
            return None

        return {
            "region": region,
            "prefix": prefix,
            "architecture": architecture,
            "ingress_controller": ingress_controller,
            "require_efs": require_efs,
        }

    @staticmethod
    def spin_up_cluster(path_to_config="config.json"):
        cfg = ClusterManager.__parse_config(path_to_config)
        if not cfg:
            print(
                "Invalid configuration file provided. Have you run '2. Configure cluster configuration?'"
            )
            return

        # Step 1: Apply Terraform
        cluster_name, region = apply_terraform()

        # Step 2: Configure kubectl for the EKS cluster
        configure_kubectl(cluster_name, region)

        # region, prefix, architecture are used in the main.tf terraform code

        # at this step, we only need to check ingress_controller and require_efs state

        if cfg["ingress_controller"] != "None":
            install_ingress_controller(cfg["ingress_controller"])

        if cfg["require_efs"] == "True":
            apply_efs_csi_driver(
                "kubernetes-sigs/aws-efs-csi-driver", ref="release-2.0"
            )

    @staticmethod
    def tear_down_cluster(path_to_config="config.json"):
        cfg = ClusterManager.__parse_config(path_to_config)
        if not cfg:
            print(
                "Invalid configuration file provided. Have you run '2. Configure cluster configuration?'"
            )
            return
        # User Prompt
        confirm = input(
            "Before tearing down the infrastructure, it is good practice to have removed all your kubernetes pods, services, and everything that was created using the kubernetes manifest. This is so as to ensure no dangling services on the cloud, such load balancers, which could cause infrastructure deprovisioning to fail. To confirm proceed, (y/N): "
        )

        if confirm == "y":

            # Clean up procedure
            # Order is important here, we are deleting in the reverse order that we created
            # create A -> create B -> create C -> destroy C -> destroy B -> destroy A
            # delete_efs_csi_driver("kubernetes-sigs/aws-efs-csi-driver", ref="release-2.0")
            if cfg["require_efs"] == "True":
                delete_efs_csi_driver(
                    "kubernetes-sigs/aws-efs-csi-driver", ref="release-2.0"
                )
            if cfg["ingress_controller"] != "None":
                delete_aws_nginx_controller()
            unconfigure_current_kubeconfig()
            destroy_terraform()
            clean_local_config_json()


# if __name__ == "__main__":
# Step 1: Apply Terraform
# cluster_name, region = apply_terraform()

# # Step 2: Configure kubectl for the EKS cluster
# configure_kubectl(cluster_name, region)

# # Step 3: Apply Kubernetes configurations
# install_aws_nginx_controller()
# apply_efs_csi_driver("kubernetes-sigs/aws-efs-csi-driver", ref="release-2.0")
