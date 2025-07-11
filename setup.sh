#!/bin/bash
set -e
cd scoutos-backend && pip install -r requirements.txt
cd ../scoutos-frontend && pnpm install

