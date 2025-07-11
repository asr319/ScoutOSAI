#!/bin/bash
set -e
cd scoutos-backend && pip install -r requirements.txt -r requirements-dev.txt
cd ../scoutos-frontend && npm install

