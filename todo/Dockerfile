FROM python:3.13-slim AS builder

# create app directory
RUN mkdir /app

# set working directory
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# production stage
FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

RUN apt -y update && apt -y install inetutils-ping bind9-host postgresql-client
# copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# set working dir
WORKDIR /app

# copy app code
COPY --chown=appuser:appuser .. .

# switch to non root user
USER appuser

# expose application port
EXPOSE 8000

# make entry file executable
RUN chmod +x /app/entrypoint.prod.sh

# start app with gunicorn
CMD ["/app/entrypoint.prod.sh"]