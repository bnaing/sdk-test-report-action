FROM ubuntu:18.04

RUN apt-get update && apt-get install -qy python3

COPY entrypoint.py /entrypoint.py

ENTRYPOINT python3 /entrypoint.py