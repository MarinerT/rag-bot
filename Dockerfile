FROM python:3.11-slim
WORKDIR /app
COPY . /app

# Set environment variables to reduce Python output buffering and not to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Initiate a virtual environment
RUN python -m venv /app/venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 5006
ENV NAME appy
ENTRYPOINT ["panel", "serve", "app.py", "--port",  "5006", "--address",  "0.0.0.0", "--allow-websocket-origin=*"]
