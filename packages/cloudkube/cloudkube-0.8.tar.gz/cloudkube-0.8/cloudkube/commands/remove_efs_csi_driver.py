from cloudkube.utils import delete_efs_csi_driver

def main():
    delete_efs_csi_driver(
        "kubernetes-sigs/aws-efs-csi-driver", ref="release-2.0"
    )
