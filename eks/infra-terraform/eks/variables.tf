# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "cluster_name" {
  type        = string
  description = "Nome do cluster a ser usado"
  default = "k8s-aws"
}

variable "cidr_block" {
  type        = string
  description = "Valor do bloco CDIR da VPC - 10.0.0.0/16"
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
  description = "Versão do cluster"
  default = "1.30"
}

variable "private_subnets" {
  type        = list(string)
  description = "Lista de subnets privadas"
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnets" {
  type        = list(string)
  description = "Lista de subnets públicas"
  default = ["10.0.4.0/24", "10.0.5.0/24"]
}

variable "lista_az" {
  type = list(string)
  description = "Lista de azs a serem usadas"
  default = ["us-east-2a", "us-east-2b"]
}