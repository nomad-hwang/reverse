FROM python:3.10-slim-bullseye

EXPOSE 80

WORKDIR /app

ADD ./project/Pipfile ./project/Pipfile.lock /app/
RUN pip3 install pipenv && pipenv install --system --deploy

ADD ./project /app

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
