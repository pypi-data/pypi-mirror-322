from cloudkube.utils import delete_aws_nginx_controller
import json



def main():

    with open("config.json", "r") as f:
        config = json.load(f)

    if config["ingressController"] == "aws-nginx-ingress-controller":
        delete_aws_nginx_controller()

    else:
        print(
            f'The ingress controller specified is {config["ingressController"]}. This is not yet supported by cloudkube.'
        )
