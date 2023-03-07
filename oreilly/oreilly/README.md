This project contains a python application that includes three APIs to query data from the database:
1) /get_book 
This API returns info about a single book. Pass work_id as query string parameter
API endpoint: http://localhost:5000?id=1

2) /get_books 
This API returns info about a specific books. Pass work_ids as POST request body. 
API endpoint: http://localhost:5000, data = {"work_ids": [1,2,3]}

3) /get_all_books: This API returns info on all the books

Build Docker image of the python app:
cd python-app
docker build -t <image_name> .
docker tag <image_name> <dockerhub_username>/<image_name>:tag
docker <dockerhub_username>/<image_name>:tag

Deploy Postgres DB and Python app on the kubernetes cluster using the mainfest files:
cd kubernetes-manifest-files
kubectl create -f postgres-deployment.yaml
kubectl create -f postgresql-service.yaml
kubectl create -f python-api-deployment.yaml
kubectl create -f python-api-service.yaml
kubectl create -f python-api-ingress.yaml




