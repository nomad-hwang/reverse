FROM python:3.10-slim-bullseye

RUN apt update && apt install openssh-server net-tools -y && \
    mkdir /var/run/sshd && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 22

VOLUME /etc
VOLUME /home
VOLUME /app

RUN sed -i 's/#GatewayPorts no/GatewayPorts yes/g' /etc/ssh/sshd_config

RUN python3 -m ensurepip && pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app
ADD ./project/Pipfile ./project/Pipfile.lock /app/
RUN pip3 install pipenv && pipenv install --system --deploy

ADD ./project /app

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
