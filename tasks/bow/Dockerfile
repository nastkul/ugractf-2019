FROM python:3.7

COPY motd /etc/motd

RUN apt-get update && apt install -y openssh-server bash libncursesw5 \
  && rm -rf /var/cache/apk/* \
  && adduser --disabled-password --no-create-home --home /app/ --gecos "" --shell /app/bow game \
  && bash -c "echo \"game:game\" | chpasswd" \
  && ssh-keygen -A \
  && mkdir /var/run/sshd

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=ru_RU.UTF-8

ENV LANG ru_RU.UTF-8 

WORKDIR /app

CMD ["/bin/bash", "-c", "/usr/sbin/sshd -D -e \"$@\""]
