FROM mariadb:10.6.5-focal

ARG MARIADB_ROOT_PASSWORD=root
ARG MARIADB_USER=root

COPY ./volume/initdb.d/ /docker-entrypoint-initdb.d/
EXPOSE 3306

CMD ["mysqld"]
