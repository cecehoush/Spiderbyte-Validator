# Base Dockerfile
FROM python:3.10-alpine

# Create a directory where code will be mounted
RUN mkdir /code

# Set the working directory
WORKDIR /code

# Install any dependencies here (optional)
# RUN pip install some-package

# The user code will be mounted to /code/script.py, so we don't need to COPY it here
CMD ["python", "/code/script.py"]
