FROM mariadb:10.6.5-focal

ENV MARIADB_ALLOW_EMPTY_ROOT_PASSWORD=yes

COPY ./initdb.d/ /docker-entrypoint-initdb.d/

CMD ["mysqld"]
