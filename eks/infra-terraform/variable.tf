# variable "driver" {
#   type        = string
#   description = "Driver used to run the minikube"
# }

variable "cluster_name" {
  type        = string
  description = "Name of the cluster to be used"
  default = "k8s-aws"
}


variable "cidr_block" {
  type        = string
  description = "Value of the VPC CIDR block - 10.0.0.0/16"
  default = "10.0.0.0/16"
}


variable "aws_profile" {
  type        = string
  description = "AWS profile for credentials"
  sensitive   = true
}


variable "var_access_key" {
  type        = string
  description = "Value of the access key used"
  sensitive = true
}

variable "var_secret_key" {
  type        = string
  description = "Value of the secret key used for access"
  sensitive = true
}

variable "cluster_version" {
  type        = string
  description = "Version of the cluster"
  default = "1.30"
}

variable "private_subnets" {
  type        = list(string)
  description = "List of private subnets"
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnets" {
  type        = list(string)
  description = "List of public subnets"
  default = ["10.0.4.0/24", "10.0.5.0/24"]
}

variable "lista_az" {
  type = list(string)
  description = "List of availability zones to be used"
  default = ["us-east-2a", "us-east-2b"]
}
