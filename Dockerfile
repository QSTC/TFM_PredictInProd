FROM python:3.8.6-buster

COPY api/ api
COPY model.joblib/ model.joblib
COPY requirements.txt/ requirements.txt
COPY TaxiFareModel/ TaxiFareModel

#NB : il est nécessaire d'avoir le dossier TaxiFareModel car il contient
#certaines classes que l'on a nous même créé et qui ne sont pas stockées
#dans le model.joblib
#par exemples certains transformer de preprocessing ou des metrics
#que l'on codé dans le dossier TaxiFareModel


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


#The host parameter will tell uvicorn to listen to all network connections
#The port parameter will tell uvicorn to listen to HTTP requests on the PORT
#environment variable configured by the cloud service running our Docker container

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
