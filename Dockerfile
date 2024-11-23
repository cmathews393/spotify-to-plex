FROM python:latest

# Set environment variables
ENV SRC_DIR /usr/bin/spotiplex/
ENV POETRY_VERSION=1.7.1
ENV PYTHONUNBUFFERED=1
ENV CRON_SCHEDULE=@daily
ENV DOCKER=True

# Accept commit SHA as a build argument
ARG COMMIT_SHA
ENV COMMIT_SHA=${COMMIT_SHA}

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy the application source code
COPY ./spotiplex ${SRC_DIR}/spotiplex
COPY pyproject.toml poetry.lock ${SRC_DIR}/
COPY README.md ${SRC_DIR}/

# Set the working directory
WORKDIR ${SRC_DIR}

# Install dependencies with Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Install supercronic
RUN wget -O /usr/local/bin/supercronic https://github.com/aptible/supercronic/releases/download/v0.1.11/supercronic-linux-amd64 \
    && chmod +x /usr/local/bin/supercronic

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Log the commit SHA during the build
RUN echo "Built from commit SHA: $COMMIT_SHA"

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
