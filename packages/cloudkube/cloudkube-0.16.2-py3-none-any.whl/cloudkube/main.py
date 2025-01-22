import argparse
from .commands.install_ingress import main as install_ingress_main
from .entry import main as entry_main
from .commands.configure_kubectl import main as configure_kubectl_main
from .commands.remove_ingress import main as remove_ingress_main
from .commands.install_efs_csi_driver import main as install_efs_csi_driver_main
from .commands.remove_efs_csi_driver import main as remove_efs_csi_driver_main


def main():
    parser = argparse.ArgumentParser(
        description="CloudKube CLI to manage cloud Kubernetes resources."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: apply-ingress
    parser_install_ingress = subparsers.add_parser(
        "install-ingress", help="Apply the ingress controller configuration"
    )
    parser_install_ingress.add_argument(
        "-c",
        "--controller",
        required=True,
        help="Specify the ingress controller to install.",
    )
    parser_init = subparsers.add_parser(
        "init", help="Starts an interactive wizard to provision cloud resources"
    )
    parser_configure_kubectl = subparsers.add_parser(
        "configure-kubectl", help="Configures .kube to hit the provisioned eks"
    )
    parser_remove_ingress = subparsers.add_parser(
        "remove-ingress", help="Removes the ingress controller from the eks"
    )
    parser_install_efs_csi_driver = subparsers.add_parser(
        "install-efs-csi-driver", help="Installs an efs-csi driver to mount efs."
    )
    parser_remove_efs_csi_driver = subparsers.add_parser(
        "remove-efs-csi-driver", help="Removes the efs-csi driver."
    )

    args = parser.parse_args()


    if args.command == "install-ingress":
        install_ingress_main(args.controller)
    elif args.command == "init":
        entry_main()
    elif args.command == "configure-kubectl":
        configure_kubectl_main()
    elif args.command == "remove-ingress":
        remove_ingress_main()
    elif args.command == "remove-efs-csi-driver":
        remove_efs_csi_driver_main()
    elif args.command == "install-efs-csi-driver":
        install_efs_csi_driver_main()


if __name__ == "__main__":
    main()
