# syntax=docker/dockerfile:1
FROM python:3.9.6

WORKDIR /home/switchdin

COPY src ./src
RUN chmod +x ./src/generator.py
RUN chmod +x ./src/aggregator.py
RUN chmod +x ./src/reporter.py