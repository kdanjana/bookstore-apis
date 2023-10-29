FROM python:3.9

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./bookstore /app
COPY ./scripts /scripts
RUN chmod +x /scripts/run.sh

WORKDIR /app
EXPOSE 8000

#need it for mysqlclient installation
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev



RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir   -r /tmp/requirements.txt && \
    rm -rf /tmp 

ENV PATH="/py/bin:$PATH"

CMD ["/scripts/run.sh"]
