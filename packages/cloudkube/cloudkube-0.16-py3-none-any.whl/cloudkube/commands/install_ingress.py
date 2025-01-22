from cloudkube.utils import install_ingress_controller
import json

ALLOWED_INGRESS_CONTROLLERS = ["aws-nginx-ingress-controller"]


def main(controller):
    with open("config.json", "r") as f:
        config = json.load(f)
        if config["ingressController"] != "None":
            print(
                f"Ingress controller {config['ingressController']} is already installed."
            )
            exit(0)

    if controller in ALLOWED_INGRESS_CONTROLLERS:
        install_ingress_controller(controller)
        with open("config.json", "w") as f:
            config["ingressController"] = controller
            json.dump(config, f, indent=4)
    else:
        print(f"The specified ingress controller '{controller}' is not supported.")
        print("Allowed ingress controllers are:")
        for controller in ALLOWED_INGRESS_CONTROLLERS:
            print(f"  - {controller}")
