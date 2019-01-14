# Flask - A simple Python CRUD application using MySQL
_By Gabriel Ferreira_

This repo shows how to create a simple Python CRUD application using MySQL and Flask web framework.
This application helps you to save deploy events in a MySQL database.
Among the included features, you'll see how to:

* POST a JSON with deploy event information;
* List resources with GET metehod;
* List a especific event passing the event ID in URI;
* DELETE deploys events passing the event ID in URI;

## You must to install locally
* Docker
* python-pip
* docker-compose (Only if you want to run this aplication docker locally)
* kubectl (Only if you want to run this aplication in a k8s cluster) 

## Installation guide
##### Clone the repo

```bash
$ git clone https://github.com/NoroFerr3ira/crud-app.git
$ cd crud-app
```

##### Run locally with docker
If you want to run this app locally using Docker, execute the command:
```bash
$ docker-compose up -d
```
After create the containers, acess http://localhost:5000/help to see how to use the API.
In this case we are usin a MySQL server in docker container, if you want to user another MySQL database just change the env vars in `docker-compose.yml` file, pointing to your MySQL server, dont forget to use `crud-app.sql` script to create the application database structure in your database.

##### Run in Kubernetes
By default, the file k8s-manifests/crud-app-deployment.yml it's using the dockr image ferr3ira/crud-app:latest, but you can change and use your Docker Hub image.
```bash
$ kubectl create -f k8s-manifests/
```
After create the service, deployment and MySQL on K8S cluster, get the URL service acess http://urlservice:port/help to see how to use the API.
In this case we are usin a MySQL server in Kubernetes cluster, if you want to user another MySQL database just change the env vars in `k8s-manifests/crud-app-deployment.yml` pointing to your MySQL server, dont forget to use `crud-app.sql` script to create the application database structure in your database.

##### Directory structure
```bash
../crud-app/
├── crud-app.sql
├── docker-compose.yml
├── Dockerfile
├── jenkins-pipelines
│   ├── crud-app-deploy.groovy
│   └── crud-app-rollback.groovy
├── k8s-manifests
│   ├── crud-app-deployment.yml
│   └── crud-app-mysql.yml
├── __main__.py
├── README.md
└── requirements.txt
```

## Obs.
In `jenkins-pipelines` directory there is two .groovy files to make a pipeline fr deploy and another to use in rollback, feel free to use this files to make your pipeline aplication.
