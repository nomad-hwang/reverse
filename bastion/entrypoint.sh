#!/bin/sh

set -e

# /etc/init.d/ssh start
/usr/sbin/sshd -D &

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 python3 /app/bastion/main.py
