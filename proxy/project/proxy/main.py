import asyncio
import logging

from proxy.apps.resolver.ssh import SSHBastionResolver
from proxy.apps.server import server
from util import aio

# import os
# from time import sleep


BASE_DOMAIN = "device.dw.heeyo.cc"

ROOT_CERT_PATH = f"/etc/letsencrypt/live/{BASE_DOMAIN}/"
CERT = ROOT_CERT_PATH + "fullchain.pem"
PRIV = ROOT_CERT_PATH + "privkey.pem"

HOST, PORT = "", 443

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format=f"%(asctime)-15s | %(levelname)-8s | [%(name)s] %(message)s",
    )

    loop = asyncio.new_event_loop()
    aio.setup_graceful_shutdown(loop)

    try:
        args = [HOST, PORT, CERT, PRIV, SSHBastionResolver(BASE_DOMAIN, None)]
        serv = server.make_forward_server(*args)
        aio.start_task(loop, serv.serve())

        loop.run_forever()
    except Exception as e:
        logging.error(e)
    finally:
        loop.close()
        logging.info("Goodbye!")
