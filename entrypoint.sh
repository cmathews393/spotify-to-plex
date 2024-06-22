echo "${CRON_SCHEDULE} poetry run spotiplex sync-lidarr-imports" > /etc/supercronic-cron
echo "${CRON_SCHEDULE} poetry run spotiplex sync-manual-lists" > /etc/supercronic-cron

poetry run spotiplex sync-manual-lists
poetry run spotiplex sync-lidarr-imports