FROM python:3.12 AS base

# RUN apt-get update && apt-get install -y ntp

# Set working directory
WORKDIR /scripts

# Copy all your script files and dependencies into the container
COPY . /scripts/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# First container-specific configuration
FROM base AS container1

# Install cron
RUN apt-get update && apt-get install -y cron

# Set the environment variable for the dbt profiles directory
ENV DBT_PROFILES_DIR=/scripts

# Copy your cron job file into the container
COPY cronjob /etc/cron.d/cronjob

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/cronjob

# Apply cron job
RUN crontab /etc/cron.d/cronjob

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD ["cron", "-f"]

# Second container-specific configuration
FROM base AS container2
CMD ["python", "airports.py"]