FROM python:3.11-slim-buster
WORKDIR /app
COPY . /app

RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential

# Set environment variables to reduce Python output buffering and not to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HNSWLIB_NO_NATIVE=1

RUN export HNSWLIB_NO_NATIVE=1

# Initiate a virtual environment
RUN python -m venv /app/venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 5006
ENV NAME appy
ENTRYPOINT ["panel", "serve", "app.py", "--port",  "5006", "--address",  "0.0.0.0", "--allow-websocket-origin=*"]
