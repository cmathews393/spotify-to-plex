#!/usr/bin/env bash

# Create the crontab file dynamically based on the passed environment variable
echo "${CRON_SCHEDULE} poetry run spotiplex sync-lidarr-imports" > /etc/supercronic-cron
echo "${CRON_SCHEDULE} poetry run spotiplex sync-manual-lists" >> /etc/supercronic-cron

# Run the initial commands
poetry run spotiplex sync-lidarr-imports
poetry run spotiplex sync-manual-lists

# Start supercronic with the generated crontab
exec supercronic /etc/supercronic-cron
