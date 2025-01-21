from cloudkube.utils import apply_efs_csi_driver


def main():
    apply_efs_csi_driver("kubernetes-sigs/aws-efs-csi-driver", ref="release-2.0")
