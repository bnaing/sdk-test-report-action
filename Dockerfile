FROM ubuntu:18.04

RUN apt-get update && apt-get install -qy python

COPY entrypoint.py /entrypoint.py

ENTRYPOINT python /entrypoint.py