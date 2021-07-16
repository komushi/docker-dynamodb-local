FROM komushi/alpine-openjdk8:3

MAINTAINER komushi

# install curl
RUN apk add --no-cache --purge -uU curl

# setup local db volume
RUN mkdir -p /var/dynamodb_local
WORKDIR /var/dynamodb_local
VOLUME ["/dynamodb_local_db"]

# download dynamodb_local
ENV DYNAMODB_VERSION=latest
ENV DYNAMODB_PORT=8080
ENV JAVA_OPTS=
RUN curl -sL -O https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_${DYNAMODB_VERSION}.tar.gz && \
    curl -sL -O https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_${DYNAMODB_VERSION}.tar.gz.sha256 && \
    sed -i "s/ .*dynamodb_local_${DYNAMODB_VERSION}.tar.gz/ *dynamodb_local_${DYNAMODB_VERSION}.tar.gz/g" dynamodb_local_${DYNAMODB_VERSION}.tar.gz.sha256 && \
    sha256sum -c dynamodb_local_${DYNAMODB_VERSION}.tar.gz.sha256 && \
    tar zxvf dynamodb_local_${DYNAMODB_VERSION}.tar.gz && \
    rm dynamodb_local_${DYNAMODB_VERSION}.tar.gz dynamodb_local_${DYNAMODB_VERSION}.tar.gz.sha256

COPY ./docker-entrypoint.sh /
COPY ./libsqlite4java-linux-arm.so /var/dynamodb_local/DynamoDBLocal_lib/
#COPY ./intarray.o /var/dynamodb_local/DynamoDBLocal_lib/
#COPY ./sqlite_wrap.o /var/dynamodb_local/DynamoDBLocal_lib/
#COPY ./sqlite3_wrap_manual.o /var/dynamodb_local/DynamoDBLocal_lib/
#COPY ./sqlite3.o /var/dynamodb_local/DynamoDBLocal_lib/

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 8080

CMD ["--sharedDb", "-dbPath", "/dynamodb_local_db"]
