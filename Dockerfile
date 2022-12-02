FROM python:3.11.0

COPY entrypoint.py /entrypoint.py

ENTRYPOINT python /entrypoint.py