
# Parsing the config.json file
variable "config_file" {
    default = "../../config.json" # Path to your JSON file
}

locals {
    config = jsondecode(file(var.config_file))
}

provider "aws" {
  region = local.config.region
}



locals {
  cluster_name = "${local.config.prefix}-eks-${random_string.suffix.result}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.1"

  name = "${local.config.prefix}-vpc"

  cidr            = "10.0.0.0/16"
  azs             = ["ap-southeast-1a", "ap-southeast-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.4.0/24", "10.0.5.0/24"]

  map_public_ip_on_launch = true
  enable_nat_gateway      = true
  single_nat_gateway      = true
  enable_dns_hostnames    = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}



module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.5"

  cluster_name    = local.cluster_name
  cluster_version = "1.30"

  cluster_endpoint_public_access           = true
  enable_cluster_creator_admin_permissions = true
  cluster_enabled_log_types                = ["api", "audit", "authenticator", "controllerManager", "scheduler"]


  cluster_addons = {
    kube-proxy = {
      version = "v1.30.0-eksbuild.3"
    }
    coredns = {
      version = "v1.11.1-eksbuild.8"
    }
    vpc-cni = {
      version = "v1.18.1-eksbuild.3"
    }
    eks-pod-identity-agent = {
      version = "v1.3.2-eksbuild.2"
    }
  }

  vpc_id = module.vpc.vpc_id

  // Attach eks to all subnets in vpc (similar to amazon launch template for eks vpc)
  # subnet_ids = concat(module.vpc.private_subnets, module.vpc.public_subnets) # TODO (@minghan): Only use private_subnets?
  subnet_ids = module.vpc.private_subnets


  eks_managed_node_group_defaults = { # This should be user selected based on architecture type of docker images
    ami_type = local.config.architecture
    # ami_type = "AL2_x86_64"
    # ami_type = "AL2_ARM_64"
  }
  # Extend node-to-node security group rules
  node_security_group_additional_rules = {
    ingress_self_all = {
      description = "Node to node all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
  }
  eks_managed_node_groups = {
    // name the nodes that are created
    one = {
      name = "node-group-1"

      instance_types = (
        local.config.architecture == "AL2_x86_64" ? ["t3.medium"] :
        local.config.architecture == "AL2_ARM_64" ? ["t4g.medium"] :
        []
      )
      # instance_types = ["t3.medium"]
      # instance_types=["t4g.medium"]

      min_size     = 2
      max_size     = 2
      desired_size = 2

      // We need to define additional iam policy so that node group can hit the s3 bucket
      iam_role_additional_policies = {
        "AmazonS3FullAccess" = "arn:aws:iam::aws:policy/AmazonS3FullAccess",
        "AmazonSSMManagedInstanceCore" : "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
      }

    }
  }
}



# Security Group for EFS with NFS Rule
resource "aws_security_group" "efs_security_group" {
  name        = "${local.config.prefix}-efs"
  description = "Security group for EFS with NFS access"
  vpc_id      = module.vpc.vpc_id # Replace with your VPC ID

  # Inbound rule to allow NFS (port 2049) access
  ingress {
    description = "Allow NFS access"
    from_port   = 2049
    to_port     = 2049
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] # Source CIDR block, adjust as needed
  }

  # Outbound rules (allow all)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.config.prefix}-efs-nfs-sg"
  }
}

// Dont need this if don't need persistent volume in kubernetes config
resource "aws_efs_file_system" "efs" {
  creation_token  = "${local.config.prefix}-efs-filesystem"
  throughput_mode = "elastic"

  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS" # Move files to Infrequent Access after 30 days
  }

  encrypted = true

}

resource "aws_efs_backup_policy" "policy" {
  file_system_id = aws_efs_file_system.efs.id
  backup_policy {
    status = "ENABLED"
  }
}

# Mount Targets for EFS (one per subnet)
resource "aws_efs_mount_target" "efs_mount_target_1" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id       = module.vpc.private_subnets[0]
  security_groups = [aws_security_group.efs_security_group.id]
}
resource "aws_efs_mount_target" "efs_mount_target_2" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id       = module.vpc.private_subnets[1]
  security_groups = [aws_security_group.efs_security_group.id]
}
