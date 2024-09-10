# Steps

1. Enable Kubernetes Engine
2. Create cluster
3. Autentificate cluster
    gcloud container clusters get-credentials <nombre-del-cluster> --zone <zona> --project <nombre-del-proyecto>
4. Deploy app
    docker build -t gcr.io/<nombre-del-proyecto>/<app-name>:latest .                                           // For Windows
    docker buildx build --platform linux/amd64 -t gcr.io/<nombre-del-proyecto>/<app-name>:latest .             // For Mac

    docker push gcr.io/<nombre-del-proyecto>/<app-name>:latest

5. Apply changes to cluster
    kubectl apply -f deployment.yaml

6. Test some fails
    - kubectl delete pod <nombre-del-pod>
    - post /crash


# Files

- collection.postman_collection.json: is the collection used for Postman with /health, /crash and /process. 
- deployment.yaml: is the kubectl file to deploy app and load balancer.  
- app.py: is the microservice with /health, /crash and /process endpoints.  
- jmeterTest.jmx: is the jmeter request file used on this experiment.
- Dockerfile: is the docker file to build image.
- requirements.txt: is the dependencie file for python app.

# Endpoints

- /health: is the health-check endpoint.
- /process: emulate the data process of something.
- /crash: launch a crash in app.

# Some details

cluster: pdg-cluster
project: api-miso
app: communication-manager

Don't forget auth and set project
    gcloud auth configure-docker
    gcloud config set project <project>
    
To confirm
    kubectl get deployments
    kubectl describe deployment <deployment-name>

    kubectl get nodes
    kubectl describe node <node-name>

    kubectl get pods
    kubectl logs <pod-name>

To rollback
    kubectl get services
    kubectl delete service <service>
    kubectl get deployments
    kubectl delete deployment <deployment>
