module "eks_cluster" {
  source = "./eks"
  cidr_block = var.cidr_block
  cluster_name = var.cluster_name
  aws_profile = var.aws_profile
  var_access_key = var.var_access_key
  var_secret_key = var.var_secret_key
  cluster_version = var.cluster_version
  private_subnets = var.private_subnets
  public_subnets = var.public_subnets
  lista_az = var.lista_az
}

# module "minikube_k8s" {
#   source = "./modules/minikube"
#   driver = var.driver
#   cluster_name = var.cluster_name
#   addons = var.addons
#   cpus = var.cpus
#   memory = var.memory
# }