FROM apache/airflow:2.10.5

# ==========================================================
# Environment
# ==========================================================

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/airflow

WORKDIR /opt/airflow

# ==========================================================
# Copy requirements
# ==========================================================

COPY --chown=airflow:root docker/requirements.txt /tmp/requirements.txt

# ==========================================================
# Install project dependencies
# ==========================================================

RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ==========================================================
# Copy project source
# ==========================================================

COPY --chown=airflow:root src ./src

# ==========================================================
# Runtime user
# ==========================================================

USER airflow