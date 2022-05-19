FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

ENV RPORTD_AUTH_USER="admin"
ENV RPORTD_AUTH_PASSWORD="shihan"
ENV RPORTD_CLIENT_PORT=8000
ENV RPORTD_API_PORT=5000
ENV TUNNEL_RANGE_PORT="20000-20050"

RUN apt update && apt install -y curl libcap2-bin

# RUN curl -o rportd-installer.sh https://get.rport.io
COPY ./scripts/rportd_installer.sh /rportd_installer.sh
RUN bash /rportd_installer.sh \
    --no-2fa \
    --client-port ${RPORTD_CLIENT_PORT} \
    --api-port ${RPORTD_API_PORT} \
    --fqdn localhost \
    --port-range ${TUNNEL_RANGE_PORT}

#1. Update rportd.conf with sed - Change the api auth by using declared <user>:<password>
##1.a Comment the database auth method
RUN sed -E -i 's/(auth_user_table\s?=\s?.*)/#\1/g' /etc/rport/rportd.conf
RUN sed -E -i 's/(auth_group_table\s?=\s?.*)/#\1/g' /etc/rport/rportd.conf
##1.b Uncomment the user/password auth method located in [api] section just before [database] and change password
RUN s_startl=`sed -n '/\[api\]/=' /etc/rport/rportd.conf` && \
    s_endl=`sed -n '/\[database\]/=' /etc/rport/rportd.conf` && \
    sed -E -i "${s_startl},${s_endl}s/(#){1,2}(auth\s?=\s?)(.*)/\2\"${RPORTD_AUTH_USER}:${RPORTD_AUTH_PASSWORD}\"/g" /etc/rport/rportd.conf

#2. Update /var/lib/rport/client-auth.json
COPY ./scripts/client-auth.json /var/lib/rport/client-auth.json

#4. Configure docker container entrypoint
COPY --chown=root:rport ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh 

USER rport
CMD ["/bin/bash","/entrypoint.sh"]

