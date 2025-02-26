FROM denoland/deno:debian-2.2.2

RUN apt update && apt install -y sudo git

# User
RUN groupadd -g 1000 -o debian
RUN useradd -m -u 1000 -g 1000 -o -s /bin/bash debian
RUN echo "debian ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
ENV PATH="/home/debian/.local/bin:${PATH}"

ENV WORKDIR /app
WORKDIR $WORKDIR

COPY . .
RUN deno install --allow-scripts

CMD ["deno", "task", "dev", "--host", "0.0.0.0"]