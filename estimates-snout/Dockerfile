FROM debian:bookworm-20250224-slim

RUN apt update && apt install -y sudo git

# User
RUN groupadd -g 1000 -o debian
RUN useradd -m -u 1000 -g 1000 -o -s /bin/bash debian
RUN echo "debian ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
ENV PATH="/home/debian/.local/bin:${PATH}"

ENV WORKDIR /app
WORKDIR $WORKDIR

# Get Bun
COPY --from=oven/bun:1.2.2-debian /usr/local/bin/bun /usr/local/bin/bun
COPY package.json .
RUN bun install

CMD ["bun", "run", "dev"]