import json
from .displayUtils import printb, printgreen


def configure_cluster_interactive():
    """
    This function provides an interactive setup for the configuration of
    the cluster.

    It will then generate the `variables.tf` file, as well as a state file for
    resources installed on the kubernetes cluster. Examples of such resources
    include:
        - nginx-ingress-controller
        - efs-csi-driver
        ...
    """
    cont = input(
        "This will override any previous configuration set in config.json. Continue? [y/N]: "
    )
    if cont != "y":
        return

    config = {}

    # Configure Region Variable
    region = input("Select Region (ap-southeast-1): ")
    # strip whitespace
    region = "".join(region.split())
    if len(region) == 0:
        # use default ap-southeast-1
        config["region"] = "ap-southeast-1"
    else:
        config["region"] = region

    # Configure Prefix Variable
    prefix = input("Set prefix of all cloud resources: ")
    config["prefix"] = prefix

    # Configure Machine Architecture
    printb("Select the architecture of your machines: ")
    print("\t1. arm (uses AL2_ARM_64)")
    print("\t2. x86 (uses AL2_x86_64)")
    arch = input("Enter a number: ")
    if arch == "1":
        config["architecture"] = "AL2_ARM_64"
    elif arch == "2":
        config["architecture"] = "AL2_x86_64"

    # Configure ingress-controller
    printb("Select (if required), and ingress controller type: ")
    print("\t 1. None")
    print("\t 2. aws-nginx-ingress-controller")
    choice = input("Enter a number: ")
    if choice == "1":
        config["ingressController"] = "None"
    elif choice == "2":
        config["ingressController"] = "aws-nginx-ingress-controller"

    # Configure efs-csi-driver
    choice = input("Do you require persistent volume setup? [y/N]")
    if choice == "y":
        config["requireEFS"] = "True"
    else:
        config["requireEFS"] = "False"

    # Save the configuration
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    print("Configuration: \n", json.dumps(config, indent=4))

    printgreen("Configuration successfully saved to config.json!")
    print("[hint]: You can now spin up your cluster by selecting option 3.")
