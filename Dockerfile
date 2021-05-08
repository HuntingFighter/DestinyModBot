FROM python:3.8.0-slim-buster
COPY ./src /app
WORKDIR /app
RUN apt-get update && apt-get install -y mariadb-client && rm -rf /var/lib/apt
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ./init_db.sh