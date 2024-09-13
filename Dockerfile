# Official dockerhub python 3.9 image
FROM python:3.9-slim

# Creating /app folder in container as usual
WORKDIR /app

# We create a virtualenv for python to avoid possible issues with dependencies and their versions
RUN python -m venv /venv

# Copying microservice /src source code to /app
COPY ./src /app

# Installing dependencies using virtualenv
RUN /venv/bin/pip install --progress-bar off --no-cache-dir -e .

# As security method and following good practices, we create an non-root user to execute the application
RUN useradd -m storage-user && chown -R storage-user /app

# We are going to use the new specific user created
USER storage-user

# Setting virtualenv environment variables
ENV VIRTUAL_ENV=/venv
ENV PATH="/venv/bin:$PATH"

# Exposing socket at port 5000 as requested
EXPOSE 5000

# Executing run.py finally to run the application
CMD ["python", "run.py"]
