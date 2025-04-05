# Use the official Miniconda image as the base image
FROM continuumio/miniconda3:latest

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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
    && apt-get clean

# Copy the requirements.txt file
COPY requirements.txt /app/

# Create a Conda environment and install dependencies
RUN conda create -n myenv python=3.11.9 && \
    echo "source activate myenv" > ~/.bashrc && \
    /opt/conda/envs/myenv/bin/pip install --upgrade pip && \
    /opt/conda/envs/myenv/bin/pip install -r requirements.txt

RUN conda install c-y onda-forge::python-chromedriver-binary 

# Set the entrypoint script
ENTRYPOINT ["/app/start_django.sh"]