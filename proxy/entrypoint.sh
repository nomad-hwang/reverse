#!/bin/sh

set -e

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 python3 /app/proxy/main.py
