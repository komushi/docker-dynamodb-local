FROM arm32v7/openjdk:8-slim

MAINTAINER komushi

# install curl
RUN apt -y update && \
    apt -y upgrade && \
    apt -y install curl

# setup local db volume
RUN mkdir -p /var/dynamodb_local
WORKDIR /var/dynamodb_local
VOLUME ["/dynamodb_local_db"]

# download dynamodb_local
ENV DYNAMODB_VERSION=2021-04-27
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

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 8080

CMD ["--sharedDb", "-dbPath", "/dynamodb_local_db"]
