FROM python:3-alpine

RUN apk add --update --no-cache socat

WORKDIR /app
EXPOSE 5000

USER nobody
CMD ["socat", "-T", "5", "tcp-l:5000,reuseaddr,fork", "exec:/app/service"]
