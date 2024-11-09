## Objective

Our goal is to maintain a single repository with the same solution deployed across three different environments:

- **Minikube** [Local]
- **EKS** [Cloud]
- **GKS** [Cloud]

This setup demonstrates Kubernetes’ flexibility, showcasing how it can remain almost completely agnostic with minimal friction, whether transitioning from on-premises to cloud or from one cloud provider to another.

### Minikube

In this case, Minikube serves as the default version. Below, I've noted the specific files modified to create this segregated environment.

> [!Note]
Some repository paths were adjusted to ensure Argo/Airflow could continue locating the necessary files.

#### Modified Files for Minikube Environment

> [!Note]
Change repo url.

(misc)
change repo path

- `minikube/manifests/misc/access-control.yaml`
- `minikube/manifests/misc/secrets.yaml`

<!-- 
(airflow if)
change repo path
- `minikube/manifests/orchestrator/airflow.yaml`
``` -->


## EKS [AWS]

A aws tem uma parada chata com o storageclass que aprendi na porrada
a maneira de armazenar storage da aws é um pouco diferente do minio e google
caçar por manifests de objetos relacionados a armazenar dados
creio que aqui seja caçar os arquivos que tenham storage class e colocar pra gp2
vou listar quais os arquivos para vc conseguir ver a diferença

- `eks/manifests/deepstorage/minio.yaml`
- `eks/manifests/database/postgres.yaml`

(misc)
change repo path

- `eks/manifests/misc/access-control.yaml`
- `eks/manifests/misc/secrets.yaml`