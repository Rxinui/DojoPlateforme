FROM mariadb:10.6.5-focal

ENV MARIADB_ALLOW_EMPTY_ROOT_PASSWORD=yes
ENV MARIADB_USER=admin
ENV MARIADB_PASSWORD=admin
ENV MARIADB_DATABASE=dojo

COPY ./volume/initdb.d/ /docker-entrypoint-initdb.d/

CMD ["mysqld"]
