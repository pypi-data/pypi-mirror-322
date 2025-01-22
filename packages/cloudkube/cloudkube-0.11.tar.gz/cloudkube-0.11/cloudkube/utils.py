# use tfenv conda environment
import boto3
import python_terraform
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
from kubernetes.utils.create_from_yaml import FailToCreateError
import yaml
import os
import requests
import tempfile
from git import Repo
import json
import subprocess


def apply_terraform():
    """Applies the Terraform configuration to create the EKS cluster."""
    terraform_dir = os.path.join(os.path.dirname(__file__), "terraform")
    tf = python_terraform.Terraform(working_dir=terraform_dir)
    return_code, stdout, stderr = tf.init()
    if return_code != 0:
        raise RuntimeError(f"Terraform init failed with error: {stderr}")
    return_code, stdout, stderr = tf.apply(auto_approve=True, capture_output=False)
    if return_code != 0:
        print("[ERROR]: Terraform apply failed")
        print(stderr)
        exit(1)
    print("[INFO]: Terraform applied successfully")
    cluster_name = tf.output("cluster_name")
    region = tf.output("region")
    return cluster_name, region


def configure_kubectl(cluster_name, region):
    """Configures local kubectl to connect to the EKS cluster."""
    print(f"region:{region}, cluster_name:{cluster_name}")
    eks = boto3.client("eks", region_name=region)
    response = eks.describe_cluster(name=cluster_name)
    cluster_endpoint = response["cluster"]["endpoint"]
    cluster_cert = response["cluster"]["certificateAuthority"]["data"]

    # Write kubeconfig
    config_data = {
        "apiVersion": "v1",
        "clusters": [
            {
                "cluster": {
                    "server": cluster_endpoint,
                    "certificate-authority-data": cluster_cert,
                },
                "name": cluster_name,
            }
        ],
        "contexts": [
            {
                "context": {"cluster": cluster_name, "user": "aws"},
                "name": cluster_name,
            }
        ],
        "current-context": cluster_name,
        "kind": "Config",
        "preferences": {},
        "users": [
            {
                "name": "aws",
                "user": {
                    "exec": {
                        "apiVersion": "client.authentication.k8s.io/v1beta1",
                        "command": "aws",
                        "args": [
                            "eks",
                            "--region",
                            region,
                            "get-token",
                            "--cluster-name",
                            cluster_name,
                        ],
                    }
                },
            }
        ],
    }

    # Ensure the .kube directory exists
    kube_dir = os.path.expanduser("~/.kube")
    os.makedirs(kube_dir, exist_ok=True)

    # Write the kubeconfig file
    kubeconfig_path = os.path.join(kube_dir, "config")
    with open(kubeconfig_path, "w") as kubeconfig:
        yaml.dump(config_data, kubeconfig)
    print("[INFO]: kubectl configured successfully")


def apply_efs_csi_driver(url, ref="release-2.0"):
    """Applies Kubernetes resources from a Kustomize directory in a GitHub repository."""

    # Clone the GitHub repository to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_url = f"https://github.com/{url}"
        print(
            f"[INFO]: apply_efs_csi_driver: Cloning {repo_url} at ref {ref} to {tmp_dir}"
        )
        Repo.clone_from(repo_url, tmp_dir, branch=ref, depth=1)

        # Locate the specific overlay directory for Kustomize
        overlay_dir = os.path.join(tmp_dir, "deploy/kubernetes/overlays/stable")

        # Use Kustomize to build the YAML from the overlay directory
        print("[INFO]: apply_efs_csi_driver: Running Kustomize to build resources...")
        result = subprocess.run(
            ["kubectl", "kustomize", overlay_dir],
            capture_output=True,
            text=True,
            check=True,
        )

        # Apply the generated YAML to the Kubernetes cluster
        config.load_kube_config()
        k8s_client = client.ApiClient()

        # Write YAML content to a temporary file and apply it
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
            temp_file.write(result.stdout)
            temp_file_path = temp_file.name

        print(
            "[INFO]: apply_efs_csi_driver: Applying Kustomize-generated resources to the cluster..."
        )
        with open("config.json", "r") as f:
            cfg = json.load(f)
        try:
            utils.create_from_yaml(k8s_client, temp_file_path)
            print(
                "[INFO]: apply_efs_csi_driver: Applied Kustomize resources successfully."
            )
            cfg["requireEFS"] = "True"
        except ApiException as e:
            print(
                f"[ERROR]: apply_efs_csi_driver: Failed to apply Kustomize resources: {e}"
            )
            cfg["requireEFS"] = "False"
        except FailToCreateError as e:
            print(f"[INFO]: apply_efs_csi_driver: EFS CSI driver already installled.")
            cfg["requireEFS"] = "True"
        finally:
            with open("config.json", "w") as f:
                json.dump(cfg, f, indent=4)


def install_ingress_controller(ingress_controller_name):
    """Installs ingress controller into the kubernetes cluster
    https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/

    Args:
        ingress_controller_name (str): refer to documentation on possible types of ingress controllers
    """
    match ingress_controller_name:
        case "aws-nginx-ingress-controller":
            install_aws_nginx_controller()
        case _:
            print("Selected ingress controller is not yet supported.")


def install_aws_nginx_controller():
    """Applies necessary Kubernetes resources using the Kubernetes client."""
    config.load_kube_config()
    k8s_client = client.ApiClient()
    url = "https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.0-beta.0/deploy/static/provider/aws/deploy.yaml"

    try:
        # Fetch YAML content from URL
        response = requests.get(url)
        response.raise_for_status()
        yaml_content = response.text

        # Write YAML content to a temporary file
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
            temp_file.write(yaml_content)
            temp_file_path = temp_file.name

        # Apply the YAML configuration
        utils.create_from_yaml(k8s_client, temp_file_path)
        print(
            f"[INFO]: install_aws_nginx_controller: Applied resource from {url} successfully"
        )

    except requests.exceptions.RequestException as e:
        print(
            f"[ERROR]: install_aws_nginx_controller: Failed to fetch resource from {url}: {e}"
        )
        with open("config.json", "r") as f:
            cfg = json.load(f)
        with open("config.json", "w") as f:
            config["ingressController"] = "None"
            json.dump(cfg, f, indent=4)

    except ApiException as e:
        print(
            f"[ERROR]: install_aws_nginx_controller: Failed to apply resource from {url}: {e}"
        )
    except FailToCreateError as e:
        print("[INFO]: nginx ingress controller already created")


def delete_resource_from_yaml(yaml_url):
    """
    Deletes Kubernetes resources defined in a YAML file using kubectl.

    Args:
        yaml_url: URL or file path to the YAML file containing resource definitions.
    """
    try:
        result = subprocess.run(
            ["kubectl", "delete", "-f", yaml_url],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"[INFO]: Deleted resources defined in {yaml_url} successfully")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR]: Failed to delete resources from {yaml_url}")
        print(e.stderr)


def delete_aws_nginx_controller():
    """Deletes the AWS NGINX Ingress Controller."""
    config.load_kube_config()
    k8s_client = client.ApiClient()
    url = "https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.0-beta.0/deploy/static/provider/aws/deploy.yaml"

    try:
        print("[INFO]: delete_aws_nginx_controller: deleting nginx controller...")
        # Fetch YAML content from URL
        response = requests.get(url)
        response.raise_for_status()
        yaml_content = response.text

        # Write YAML content to a temporary file
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
            temp_file.write(yaml_content)
            temp_file_path = temp_file.name

        # Delete the YAML configuration
        delete_resource_from_yaml(temp_file_path)
        print(
            "[INFO]: delete_aws_nginx_controller: Deleted NGINX Ingress Controller successfully."
        )
        with open("config.json", "r") as f:
            cfg = json.load(f)
        cfg["ingressController"] = "None"
        with open("config.json", "w") as f:
            json.dump(cfg, f, indent=4)

    except requests.exceptions.RequestException as e:
        print(
            f"[ERROR]: delete_aws_nginx_controller: Failed to fetch resource from {url}: {e}"
        )
    except ApiException as e:
        print(f"[ERROR]: delete_aws_nginx_controller: Failed to delete resource: {e}")


def delete_efs_csi_driver(url, ref="release-2.0"):
    """Deletes Kubernetes resources from a Kustomize directory in a GitHub repository."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_url = f"https://github.com/{url}"
        print(
            f"[INFO]: delete_efs_csi_driver: Cloning {repo_url} at ref {ref} to {tmp_dir}"
        )
        Repo.clone_from(repo_url, tmp_dir, branch=ref, depth=1)
        overlay_dir = os.path.join(tmp_dir, "deploy/kubernetes/overlays/stable")

        print("[INFO]: delete_efs_csi_driver: Running Kustomize to build resources...")
        result = subprocess.run(
            ["kubectl", "kustomize", overlay_dir],
            capture_output=True,
            text=True,
            check=True,
        )

        config.load_kube_config()
        k8s_client = client.ApiClient()

        with tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
            temp_file.write(result.stdout)
            temp_file_path = temp_file.name

        print(
            "[INFO]: delete_efs_csi_driver: Deleting Kustomize-generated resources from the cluster..."
        )
        with open("config.json", "r") as f:
            cfg = json.load(f)
        try:
            delete_resource_from_yaml(temp_file_path)
            print(
                "[INFO]: delete_efs_csi_driver: Deleted Kustomize resources successfully."
            )
            cfg["requireEFS"] = "False"
        except ApiException as e:
            print(
                f"[ERROR]: delete_efs_csi_driver: Failed to delete Kustomize resources: {e}"
            )
            cfg["requireEFS"] = "True"
        finally:
            with open("config.json", "w") as f:
                json.dump(cfg, f, indent=4)


# TODO: This does not clean ~/.kube/config that well, we can think of making this better
def unconfigure_current_kubeconfig():
    try:
        # Get the current context name
        current_context_result = subprocess.run(
            ["kubectl", "config", "current-context"],
            capture_output=True,
            text=True,
            check=True,
        )
        current_context_name = current_context_result.stdout.strip()

        # user_confirm = input(
        #     f"This will delete context {current_context_name}. Continue? (y/N): "
        # )

        # if user_confirm == "y":
        # Delete the current context
        subprocess.run(
            ["kubectl", "config", "delete-context", current_context_name],
            check=True,
        )

        # Unset the user and cluster for the current context
        subprocess.run(
            ["kubectl", "config", "unset", f"users.{current_context_name}"], check=True
        )
        subprocess.run(
            ["kubectl", "config", "unset", f"clusters.{current_context_name}"],
            check=True,
        )

        print(
            f"[INFO]: Successfully removed current context '{current_context_name}' from kubeconfig"
        )

        # else:
        # print("[INFO]: context is not deleted.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR]: Failed to unconfigure kubeconfig for current context: {e}")


def destroy_terraform():
    """Destroys the Terraform-managed infrastructure."""
    terraform_dir = os.path.join(os.path.dirname(__file__), "terraform")
    tf = python_terraform.Terraform(working_dir=terraform_dir)

    # Execute the destroy command without unnecessary flags
    return_code, stdout, stderr = tf.destroy(
        auto_approve=True, force=None, capture_output=False
    )

    if return_code != 0:
        print("[ERROR]: Terraform destroy failed")
        print(stderr)
        exit(1)

    print("[INFO]: Terraform destroy completed successfully")


def clean_local_config_json():
    subprocess.run(["rm", "-f", "config.json"])
