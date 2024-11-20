# [IN DEV]

## LAB | K8-SPOK(DELTA)-AIRFLOW-MINIO [MINIKUBE]

The objective of this repository is to upgrade a [solution](https://github.com/Gabriel-Philot/Case_Breweries_Abinbev) that was originally built outside of the Kubernetes environment and bring it into Kubernetes.

First of all, I want to thanks [GersonRS](https://github.com/GersonRS) for the amazing [repository](https://github.com/GersonRS/hands-on-running-spark-jobs-with-airflow) that made this lab possible (perfect guide).

>[!Note]
> To understand how to proceed/use this project, refer to the (repo -> instructions) general & pre-full-guide. I’ll improve the docs/readme as the project evolves.


### Completed : 

* Process v0
* Fix ingestion (look in instructions - pre-total-guide.md)
* Configured jupyter lab with DuckDb configs to acess Minio-Lakehouse data.
* Minikube v0 done

### In Dev:

* Protheus or grafana (Still needs metrics)
* Good practices airflow (still need polish)
* Deploy it on AWS (EKS). | Still need to see how to enable weebhoook.

### Next Steps:

* Deploy it in GCP
* CI/CD
* Data Catalog