FROM python:latest

# Set environment variables
ENV SRC_DIR /usr/bin/spotiplex/
ENV POETRY_VERSION=1.2.0
ENV PYTHONUNBUFFERED=1
ENV CRON_SCHEDULE="0 0 * * *"

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy the application source code
COPY ./spotiplex ${SRC_DIR}/
COPY pyproject.toml poetry.lock ${SRC_DIR}/

# Set the working directory
WORKDIR ${SRC_DIR}

# Install dependencies with Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Install supercronic
RUN wget -O /usr/local/bin/supercronic https://github.com/aptible/supercronic/releases/download/v0.1.11/supercronic-linux-amd64 \
    && chmod +x /usr/local/bin/supercronic

# Copy the script to generate the cron file
COPY generate_cron.sh /usr/local/bin/generate_cron.sh
RUN chmod +x /usr/local/bin/generate_cron.sh

# Set the command to generate the cron file and run supercronic
CMD ["/bin/sh", "-c", "/usr/local/bin/generate_cron.sh && /usr/local/bin/supercronic /etc/supercronic-cron"]


