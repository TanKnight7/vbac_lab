#!/bin/bash
docker rm vbac_lab || true
docker rmi vbac_lab || true
docker build -t vbac_lab .
docker run -d -p 8000:8000 --name vbac_lab vbac_lab