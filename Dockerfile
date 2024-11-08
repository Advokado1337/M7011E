FROM python:3.12

ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]