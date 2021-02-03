# Create the sync-gandi-dns Python application image.
FROM python:3.7-alpine3.11 AS sync-gandi-dns

ARG BUILD_TAG=local
LABEL build_tag=${BUILD_TAG}
LABEL description="sync-gandi-dns - Python Application"

# Configure the cron jobs.
COPY /docker/crontab.txt /crontab.txt
RUN /usr/bin/crontab /crontab.txt

# Set scheduler to run.
COPY /docker/entry.sh /entry.sh
RUN chmod +x /entry.sh

CMD ["/entry.sh"]

# Create a folder to install the application from.
WORKDIR /src

# Copy and install the application.
COPY . .
RUN pip3 install -U .
