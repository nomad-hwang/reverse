#!/bin/sh

domain="*.device.example.com"

docker run -it --rm --name certbot \
  -v '/etc/letsencrypt:/etc/letsencrypt' \
  -v '/var/lib/letsencrypt:/var/lib/letsencrypt' \
  certbot/certbot certonly -d domain --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory

# Register cronjob to renew certificate every day at 3am
sudo crontab -l | { cat; echo "0 3 * * * docker run -it --rm --name certbot -v '/etc/letsencrypt:/etc/letsencrypt' -v '/var/lib/letsencrypt:/var/lib/letsencrypt' certbot/certbot renew"; } | sudo crontab -