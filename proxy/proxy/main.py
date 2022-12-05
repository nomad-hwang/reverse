import asyncio
import logging

from proxy.apps.resolver.bastion import SSHBastionResolver
from proxy.apps.server import server
from proxy.config import settings

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format=f"%(asctime)-15s | %(levelname)-8s | [%(name)s] %(message)s",
    )

    loop = asyncio.new_event_loop()

    try:
        serv = server.make_forward_server(
            host=settings.HOST,
            port=settings.PORT,
            cert_path=settings.CERT_PATH,
            key_path=settings.KEY_PATH,
            resolver=SSHBastionResolver(settings.BASE_DOMAIN),
        )
        task = loop.create_task(serv.serve())

        loop.run_forever()
    except Exception as e:
        logging.error(e)
    finally:
        loop.close()
        logging.info("Goodbye!")
