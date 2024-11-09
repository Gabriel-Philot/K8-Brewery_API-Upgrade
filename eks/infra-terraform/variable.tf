# variable "driver" {
#   type        = string
#   description = "Driver usado para executar o minikube"
# }

variable "cluster_name" {
  type        = string
  description = "Nome do cluster a ser usado"
  default = "k8s-aws"
}

# variable "addons" {
#   type = list(string)
#   description = "Adicionais de configuração do cluster"
# }

# variable "cpus" {
#   type        = number
#   description = "Numero de CPUs usadas"
# }

# variable "memory" {
#   type        = string
#   description = "Quantidade de memória"
# }

variable "cidr_block" {
  type        = string
  description = "Valor do bloco CDIR da VPC - 10.0.0.0/16"
  default = "10.0.0.0/16"
}

variable "var_access_key" {
  type        = string
  description = "Valor da chave de acesso usada"
  default = ""
}

variable "var_secret_key" {
  type        = string
  description = "Valor da secret usada para o acesso"
  default = ""
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
  default = ["us-east-1a", "us-east-1b"]
}