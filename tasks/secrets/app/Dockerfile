FROM python:3-alpine

WORKDIR /app

RUN apk --no-cache --update add socat

COPY app /app

CMD ["socat", "tcp-l:1337,reuseaddr,fork", "exec:/app/server.py"]
EXPOSE 1337

