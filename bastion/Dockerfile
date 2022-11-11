FROM linuxserver/openssh-server

RUN sed -i 's/AllowTcpForwarding no/AllowTcpForwarding yes/g' /etc/ssh/sshd_config
RUN sed -i 's/GatewayPorts no/GatewayPorts yes/g' /etc/ssh/sshd_config
RUN sed -i 's/X11Forwarding no/X11Forwarding yes/g' /etc/ssh/sshd_config

RUN apk add --update --no-cache python3 lsof gcc build-base linux-headers py3-psutil && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app
ADD ./project/Pipfile ./project/Pipfile.lock /app/
RUN pip3 install pipenv && pipenv install --system --deploy

ADD ./project /app

CMD ["/bin/sh", "-c", "PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 /usr/bin/python /app/bastion/main.py"]

ENTRYPOINT ["/init"]
