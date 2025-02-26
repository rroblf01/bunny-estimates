FROM python:3.13.2-slim-bookworm

ARG INSTALL_DEV_DEPENDENCIES
RUN apt update && apt install -y sudo git

# User
RUN groupadd -g 1000 -o debian
RUN useradd -m -u 1000 -g 1000 -o -s /bin/bash debian
RUN echo "debian ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
ENV PATH="/home/debian/.local/bin:${PATH}"

ENV WORKDIR /app
WORKDIR $WORKDIR
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

COPY pyproject.toml /tmp/pyproject.toml

RUN rm /usr/local/bin/pip
COPY --from=ghcr.io/astral-sh/uv:0.6.2-python3.13-bookworm-slim /usr/local/bin/uv /usr/local/bin/uv
RUN uv pip install --system -r /tmp/pyproject.toml ${INSTALL_DEV_DEPENDENCIES}

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]