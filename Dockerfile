# syntax=docker/dockerfile:1.2
FROM python:latest
# put you docker configuration here
COPY ./requirements.txt /requirements.txt

#
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

#
COPY ./challenge ./challenge

# the service should be able to load it from external source in case you update the model, but for now i will copy it locally
COPY model.sav ./model.sav

# 
CMD ["uvicorn", "challenge:api.app", "--host", "0.0.0.0", "--port", "80"]