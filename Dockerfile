FROM python:3.11.12-slim-bookworm


# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Make the start_django.sh script executable
RUN chmod +x start_django.sh

# Install MySQL driver and other necessary packages
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    default-mysql-client \
    wget \
    unzip \
    curl \
    && apt-get clean

# Install Google Chrome and ChromeDriver
# Dockerfile
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get update && apt-get install -y \
google-chrome-stable \
libglib2.0-0 \
&& rm -rf /var/lib/apt/lists/*

RUN DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
wget https://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip && \
unzip chromedriver_linux64.zip -d /usr/bin/ && rm chromedriver_linux64.zip && chmod +x /usr/bin/chromedriver

ENV CHROMEDRIVER=/usr/bin/chromedriver
RUN pip install -r requirements.txt

ENTRYPOINT ["/app/start_django.sh"]