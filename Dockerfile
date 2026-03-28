# Step 1: Start from official Python image
FROM python:3.12-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy requirements first (for caching)
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your project
COPY . .

# Step 6: Tell Docker which port Django runs on
EXPOSE 8000

# .env is not in the image by default (.dockerignore). Inject at run time, e.g.:
#   docker run -p 8000:8000 --env-file .env my-django-app
# If Postgres runs on the host (Docker Desktop), set DB_HOST=host.docker.internal in .env or -e.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]