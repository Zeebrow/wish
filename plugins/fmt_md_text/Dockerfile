FROM golang:1.17

ARG BIN_OUTPUT_NAME=fmt_md_text

WORKDIR /app
COPY . .
RUN mkdir /output && go build -o /output/$BIN_OUTPUT_NAME .
