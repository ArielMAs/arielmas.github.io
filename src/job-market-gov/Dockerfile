FROM ubuntu:latest

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && apt-get install -y curl \
                                         jq \
                                         python3.12 \
                                         && rm -rf /var/lib/apt/lists/*


# Copy the project into the image
COPY pyproject.toml run.sh uv.lock job-market-gov/job_listing.py .

# Define build arguments
ARG API_EMAIL
ARG API_AUTH

# Set environment variables from build arguments
ENV API_EMAIL=${API_EMAIL}
ENV API_AUTH=${API_AUTH}

# Give execute permissions to the shell script
RUN chmod +x ./run.sh && ./run.sh

# Create a virtual environment and install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv sync --frozen && \
    python3 job_listing.py main.json --first_run True

