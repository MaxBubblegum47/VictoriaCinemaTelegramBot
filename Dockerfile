# Use the official Python image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the script and requirements file into the container
COPY src/main.sh src/requirements.txt src/helper_main.sh src/helper_movie.sh src/info.py src/main.py src/movie.py src/config.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the script as the entry point
ENTRYPOINT ["bash", "main.sh"]
