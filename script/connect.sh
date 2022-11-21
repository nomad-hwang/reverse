#!/bin/sh

ENDPOINT="device.exmple.com"
ENDPOINT_API_PORT="2223"
ENDPOINT_SSH_PORT="2222"

DEVICE_NAME="$(cat /etc/machine-id)"

PRI_KEY_PATH="/etc/reverse_client.d/key_ed25519"
PUB_KEY_PATH="/etc/reverse_client.d/key_ed25519.pub"

if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# generate key pair
if [ ! -f $PUB_KEY_PATH ]; then
    mkdir -p /etc/reverse_client.d
    ssh-keygen -t ed25519 -f $PRI_KEY_PATH -N ""
    chmod 600 $PRI_KEY_PATH
    chmod 644 $PUB_KEY_PATH
fi

# Register device
register_device() {
    echo "Registering device..."
    curl -X 'POST' \
    "${ENDPOINT}:${ENDPOINT_API_PORT}/api/v1/device" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
        "name": "'"${DEVICE_NAME}"'",
        "ssh_key": "'"$(cat $PUB_KEY_PATH)"'"
    }'
}

while true; do
    echo "Check if the device is already registered..."
    register_device
    echo
    echo "Connecting to the server ${ENDPOINT_SSH}:${ENDPOINT_SSH_PORT} as ${DEVICE_NAME}"
    ssh -N -R0 ${DEVICE_NAME}@${ENDPOINT} -p ${ENDPOINT_SSH_PORT} -i ${PRI_KEY_PATH} -o StrictHostKeyChecking=no

    echo "Disconnected from the server. Retrying in 10 seconds..."
    sleep 10
done