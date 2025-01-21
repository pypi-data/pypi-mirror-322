# ---------------------------
# 1) Base Stage
# ---------------------------
FROM python:3.11-slim AS base

# Set required environment variables.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Build-time arguments
ARG AGENT_SRC_PATH=./agent_src
ARG DEPLOYMENT_ID=default-deployment-id

# Persist deployment ID at runtime
ENV JAY_INTERNAL__DEPLOYMENT_ID=${DEPLOYMENT_ID}

WORKDIR /app

# Create a virtual environment.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip.
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements and install them.
COPY ${AGENT_SRC_PATH}/requirements.txt agent_src/requirements.txt
RUN pip install --no-cache-dir -r agent_src/requirements.txt

# Copy the agent source code.
COPY ${AGENT_SRC_PATH} ./agent_src

# Dynamically create a server.py that calls config.create_production_api().
RUN echo "from agent_src.main import config\nfrom jay_ai.loader import load_agent\nagent = load_agent('agent_src/main.py')\napp = agent.create_production_api()" \
    > ./agent_src/server.py

# ---------------------------
# 2) Dev Stage (copies jay_ai and associated pyproject.toml)
# ---------------------------
FROM base AS dev

# This build argument defines the local package source path.
# (For example, you might pass: --build-arg LOCAL_PACKAGE_PATH=tmp/jay_ai)
ARG LOCAL_PACKAGE_PATH

# Copy the local jay_ai files into a temporary folder only if they exist.
# Also copy the pyproject.toml from one directory above.
# (Assumes that the local package path is relative and that ../pyproject.toml exists relative to it.)
COPY ${LOCAL_PACKAGE_PATH} /tmp
COPY ${LOCAL_PACKAGE_PATH}/pyproject.toml /tmp/pyproject.toml

# If local jay_ai is used, uninstall the published package and reinstall from the local source.
RUN echo "Installing local jay_ai from /tmp/jay_ai..." \
    && mkdir -p /app/package \
    && cp -r /tmp/jay_ai /app/package/jay_ai \
    && cp /tmp/pyproject.toml /app/package/pyproject.toml \
    && rm -rf /tmp/jay_ai /tmp/pyproject.toml \
    && pip uninstall -y jay_ai || true \
    && pip install --no-cache-dir /app/package

# Final command for the dev stage.
CMD ["gunicorn", "agent_src.server:app", "-w", "4", "-k", "uvicorn_worker.UvicornWorker", "--bind", "0.0.0.0:10000", "--log-level", "debug", "--access-logfile", "-"]

# ---------------------------
# 3) Prod Stage (no jay_ai folder)
# ---------------------------
FROM base AS prod
# Do not copy any local jay_ai. (The published package from requirements will be used.)
CMD ["gunicorn", "agent_src.server:app", "-w", "4", "-k", "uvicorn_worker.UvicornWorker", "--bind", "0.0.0.0:10000", "--log-level", "debug", "--access-logfile", "-"]