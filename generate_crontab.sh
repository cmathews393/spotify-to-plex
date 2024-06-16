#!/bin/sh

# Generate the cron file based on environment variables
echo "${CRON_SCHEDULE} poetry run spotiplex sync-lidarr-imports" > /etc/supercronic-cron
echo "${CRON_SCHEDULE} poetry run spotiplex sync-manual-lists" > /etc/supercronic-cron
