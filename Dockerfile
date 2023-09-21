FROM golang:1.16 AS builder

USER root

# Download and build all prerequisites
WORKDIR /
RUN git clone https://github.com/insidersec/insider.git

WORKDIR /insider
RUN go mod download
RUN make build-release

FROM alpine:latest

WORKDIR /opt/insider

# Copy the build
COPY --from=builder /insider /opt/insider/insider

# Link the babuska
RUN ln -s /opt/insider/insider/insider /usr/local/bin/insider

# Install extra dependencies
RUN apk update
RUN apk add jq grep python3 curl

# Copy the entrypoint
WORKDIR /
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY report.py /report.py
RUN chmod +x /report.py

# Create a user
RUN adduser -D -g '' user
USER user
WORKDIR /data

ENTRYPOINT ["/entrypoint.sh"]
